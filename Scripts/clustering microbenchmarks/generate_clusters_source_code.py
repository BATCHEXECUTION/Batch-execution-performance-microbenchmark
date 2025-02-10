import os
import glob

# JMH_BENCHMARKS_DIR = "/Users/mj/workspace/RxJava/src/jmh/java/"  
JMH_BENCHMARKS_DIR = "/Users/mj/workspace/eclipse-collections/jmh-tests/src/main/java/"

def read_benchmarks_from_file(file_path):
    """
    Reads benchmarks and their associated methods from a file.
    Example: "BenchmarkName: method1, method2, method3"
    """
    benchmarks = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                benchmark_name, methods = line.split(':')
                method_list = methods.split(',')
                benchmarks[benchmark_name.strip()] = [method.strip() for method in method_list]
    return benchmarks

def find_java_file_for_class(class_name):
    """ Constructs the expected Java file path from class_name instead of searching. """
    java_file_path = os.path.join(
        JMH_BENCHMARKS_DIR, 
        class_name.replace('.', '/').split('/_')[0] + ".java"
    )
    return java_file_path if os.path.exists(java_file_path) else None


def contains_run_benchmark(java_file, method_name):
    """ Checks if the Java file contains 'this.runBenchmark(this.payloads.<method_name>);' in the method. """
    if not java_file:
        return False
    with open(java_file, 'r', encoding='utf-8') as file:
        content = file.read()
        return f"this.runBenchmark(this.payloads.{method_name});" in content

def generate_merged_benchmark_class(benchmark_name, methods):
    """ Generates a Java class for a merged benchmark. """

#     # class_template = """package io.reactivex.rxjava3.core.clusters;
#     class_template = """package org.eclipse.collections.impl.clusters;



# public class {benchmark_name} {{

#    @org.openjdk.jmh.annotations.State(org.openjdk.jmh.annotations.Scope.Thread)
#     public static class _Benchmark {{

#        {fields}

#         @org.openjdk.jmh.annotations.Setup(org.openjdk.jmh.annotations.Level.Trial)
#         public void makePayloads() {{
#             {instantiations}
#             {make_payload_calls}
#         }}
        
#         @org.openjdk.jmh.annotations.Benchmark
#         public void benchmark_{benchmark_name}() throws java.lang.Throwable {{
#             {evaluate_calls}
#         }}

#    }}

# }}"""

    # class_template = """package io.reactivex.rxjava3.core.clusters;
    class_template = """package zipkin2.clusters;


public class {benchmark_name} {{

   @org.openjdk.jmh.annotations.State(org.openjdk.jmh.annotations.Scope.Thread)
    public static class _Benchmark {{

       {fields}
        
        @org.openjdk.jmh.annotations.Setup(org.openjdk.jmh.annotations.Level.Trial)
        public void makePayloads() {{
            {instantiations}
        }}

        @org.openjdk.jmh.annotations.Benchmark
        public void benchmark_{benchmark_name}() throws java.lang.Throwable {{
            {evaluate_calls}
        }}

   }}

}}"""


    fields = []
    instantiations = []
    make_payload_calls = []
    evaluate_calls = []
    created_classes = {}

    for i, method in enumerate(methods):
        if '.' not in method:
            # print(f"Skipping invalid method name: {method}")
            continue  
        
        class_name, method_name = method.rsplit('.', 1)
        class_short_name = class_name.split('.')[-1]  

        if class_name not in created_classes:
            field_name = f"{class_short_name}_benchmark_{i}"
            fields.append(f"private {class_name} {field_name};")
            instantiations.append(f"{field_name} = new {class_name}();")
            created_classes[class_name] = field_name  

        field_name = created_classes[class_name]

        make_payload_calls.append(f"this.{field_name}.makePayloads();")

        # Find the Java file for this benchmark class
        java_file = find_java_file_for_class(class_name)

        # Check if the benchmark method uses `this.runBenchmark(this.payloads.<method_name>);`
        if contains_run_benchmark(java_file, method_name.replace("benchmark_", "")):
            # evaluate_calls.append(f"this.{field_name}.createImplementation();")
            # evaluate_calls.append(f"this.{field_name}.runBenchmark(this.{field_name}.implementation()::{method_name.replace('benchmark_', '')},this.{field_name}.description(\"{method_name.replace('benchmark_', '')}\"));")
            evaluate_calls.append(f"this.{field_name}.runBenchmark(this.{field_name}.payloads.{method_name.replace('benchmark_', '')});")
        else:
            evaluate_calls.append(f"this.{field_name}.payloads.{method_name.replace('benchmark_', '')}.evaluate();")

    java_class = class_template.format(
        benchmark_name=benchmark_name,
        fields="\n       ".join(fields),
        instantiations="\n            ".join(instantiations),
        make_payload_calls="\n            ".join(make_payload_calls),
        evaluate_calls="\n            ".join(evaluate_calls),
    )

    return java_class

def main():
    input_file = 'clusters_ready_to_generate_file.txt'
    benchmarks = read_benchmarks_from_file(input_file)
    
    output_dir = 'clusters'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for benchmark_name, methods in benchmarks.items():
        java_class_code = generate_merged_benchmark_class(benchmark_name, methods)
        
        output_file = os.path.join(output_dir, f"{benchmark_name}.java")
        with open(output_file, 'w') as java_file:
            java_file.write(java_class_code)
        print(f"Generated: {output_file}")

if __name__ == "__main__":
    main()
