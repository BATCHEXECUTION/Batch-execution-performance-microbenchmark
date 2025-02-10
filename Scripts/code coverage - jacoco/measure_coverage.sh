#!/bin/bash

# Path to the JAR file containing JMH benchmarks
JMH_JAR_FILE="path_to_jmh.jar"
# Example:
# JMH_JAR_FILE="RxJava/build/libs/rxjava-3.0.0-SNAPSHOT-jmh.jar"
# JMH_JAR_FILE="eclipse-collections/jmh-tests/target/microbenchmarks.jar"
# JMH_JAR_FILE="zipkin/benchmarks/target/benchmarks.jar" << ju2jmh benchmarks are here
# JMH_JAR_FILE="zipkin/benchmarks/target/original-benchmarks.jar" << hand-crafted jmh benchmarks are here

# Path to the text file containing the list of JMH benchmarks
BENCHMARK_LIST="benchmark_list.txt"

# Output directory for individual coverage reports
OUTPUT_DIR="output_directory"

# Path to JaCoCo agent JAR
JACOCO_AGENT_JAR="/path_to_jacoco_agent_jar/org.jacoco.agent.jar"

# Path to JaCoCo CLI JAR
JACOCO_CLI_JAR="/path_to_jacoco_cli_jar/org.jacoco.cli.jar"

# Path to binary classes
CLASS_FILES_MAIN=="/path_to_binary_classes/"
# Example:
# CLASS_FILES_MAIN="RxJava/build/classes/"
# CLASS_FILES_MAIN="eclipse-collections/eclipse-collections/target/classes/"
# CLASS_FILES_MAIN="zipkin/zipkin/target/classes/"


# Python script to convert XML report to CSV
PYTHON_SCRIPT="jacoco_xml_to_csv_only_covered_lines.py"

# Ensure the required files and directories exist
if [[ ! -f "$JMH_JAR_FILE" ]]; then
    echo "Error: JAR file not found at $JMH_JAR_FILE"
    exit 1
fi

if [[ ! -f "$BENCHMARK_LIST" ]]; then
    echo "Error: Benchmark list file not found at $BENCHMARK_LIST"
    exit 1
fi

if [[ ! -f "$JACOCO_AGENT_JAR" ]]; then
    echo "Error: JaCoCo agent JAR not found at $JACOCO_AGENT_JAR"
    exit 1
fi

if [[ ! -f "$JACOCO_CLI_JAR" ]]; then
    echo "Error: JaCoCo CLI JAR not found at $JACOCO_CLI_JAR"
    exit 1
fi

if [[ ! -d "$CLASS_FILES" ]]; then
    echo "Error: Binary classes directory not found at $CLASS_FILES"
    exit 1
fi

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# JMH configurations to capture coverage data (no warmup, 1 iteration, single shot mode)
JMH_CONFIG="-f 1 -wi 0 -i 1 -r 1 -w 1 -bm ss -foe true"

# Iterate over each benchmark in the list
while IFS= read -r benchmark || [[ -n "$benchmark" ]]; do
    # Skip empty lines or comments
    if [[ -z "$benchmark" || "$benchmark" =~ ^# ]]; then
        continue
    fi

    echo "Processing benchmark: $benchmark"

    # Create directory for the benchmark
    benchmark_dir="$OUTPUT_DIR/$benchmark"
    mkdir -p "$benchmark_dir"

    # Run JMH benchmark with JaCoCo agent and generate coverage report
    java -javaagent:"$JACOCO_AGENT_JAR"=output=file,destfile="$benchmark_dir/coverage.exec" \
         -jar "$JMH_JAR_FILE" "$benchmark\$" $JMH_CONFIG

    # Check if the coverage execution file was generated
    if [[ ! -f "$benchmark_dir/coverage.exec" ]]; then
        echo "Error: Coverage file not generated for $benchmark"
        continue
    fi

    # Generate code coverage report in XML format
    java -jar "$JACOCO_CLI_JAR" report "$benchmark_dir/coverage.exec" \
         --classfiles "$CLASS_FILES_MAIN=" \
         --xml "$benchmark_dir/report.xml"

    # Convert XML report to CSV using the Python script
    if [[ -f "$PYTHON_SCRIPT" ]]; then
        python3 "$PYTHON_SCRIPT" "$benchmark_dir/report.xml" "$benchmark_dir/report.csv"
        # Remove the XML report after successful conversion
        rm -f "$benchmark_dir/report.xml" "$benchmark_dir/coverage.exec"
    else
        echo "Warning: Python script $PYTHON_SCRIPT not found. Skipping XML to CSV conversion."
    fi
done < "$BENCHMARK_LIST"
