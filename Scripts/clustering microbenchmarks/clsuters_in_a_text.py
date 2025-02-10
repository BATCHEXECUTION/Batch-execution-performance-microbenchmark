import os
import csv
from typing import Dict, List, Tuple

# Type aliases for better readability
Ju2JmhBenchmark = Tuple[str, float, float, float]  # Name, Throughput, Runtime, Score
BenchmarkData = Dict[str, List[Ju2JmhBenchmark]]

# Function to group ju2jmh benchmarks
def clusters_all_possible(benchmark_data: BenchmarkData, threshold: float) -> Dict[str, List[List[Ju2JmhBenchmark]]]:
    """
    Groups ju2jmh benchmarks for each JMH benchmark based on a runtime threshold.

    Args:
        benchmark_data: Dictionary mapping JMH benchmarks to their ju2jmh benchmarks (name, throughput, runtime, score).
        threshold: The maximum cumulative runtime for a group.

    Returns:
        A dictionary mapping JMH benchmarks to their groups of ju2jmh benchmarks.
    """
    grouped_data = {}
    used_benchmarks = set()  # To track which benchmarks have already been grouped

    for jmh_benchmark, ju2jmh_list in benchmark_data.items():
        # Filter out benchmarks with runtime exceeding the threshold or already grouped
        valid_ju2jmh_list = [
            benchmark for benchmark in ju2jmh_list
            # if benchmark[2] <= threshold and benchmark[0] not in used_benchmarks
            if benchmark[2] <= threshold 
        ]

        # Sort ju2jmh benchmarks by similarity score in descending order
        valid_ju2jmh_list.sort(key=lambda x: x[3], reverse=True)
        
        groups = []
        current_group = []
        current_runtime = 0.0

        while valid_ju2jmh_list:
            # Get the ju2jmh benchmark with the highest similarity score
            ju2jmh_benchmark = valid_ju2jmh_list.pop(0)
            runtime = ju2jmh_benchmark[2]

            if current_runtime + runtime <= threshold:
                current_group.append(ju2jmh_benchmark)
                current_runtime += runtime
                # used_benchmarks.add(ju2jmh_benchmark[0])  # Mark as used
            else:
                # Finalize the current group and start a new one
                if current_group:
                    groups.append(current_group)
                current_group = [ju2jmh_benchmark]
                current_runtime = runtime
                # used_benchmarks.add(ju2jmh_benchmark[0])  # Mark as used

        # Add the last group if it's not empty
        if current_group:
            groups.append(current_group)

        grouped_data[jmh_benchmark] = groups

    return grouped_data

# Function to group ju2jmh benchmarks
def clusters_highest_overlap(benchmark_data: BenchmarkData, threshold: float) -> Dict[str, List[List[Ju2JmhBenchmark]]]:
    """
    Groups ju2jmh benchmarks for each JMH benchmark based on a runtime threshold.

    Args:
        benchmark_data: Dictionary mapping JMH benchmarks to their ju2jmh benchmarks (name, throughput, runtime, score).
        threshold: The maximum cumulative runtime for a group.

    Returns:
        A dictionary mapping JMH benchmarks to their groups of ju2jmh benchmarks.
    """

    all_ju2jmh_benchmarks = set()  # To track which benchmarks have already been grouped
    for jmh_benchmark, ju2jmh_list in benchmark_data.items():
        # Filter out benchmarks with runtime exceeding the threshold or already grouped
        valid_ju2jmh_list = [
            benchmark for benchmark in ju2jmh_list
            if benchmark[2] <= threshold
        ]

        while valid_ju2jmh_list:
            # Get the ju2jmh benchmark with the highest similarity score
            ju2jmh_benchmark = valid_ju2jmh_list.pop(0)
            if(ju2jmh_benchmark[0] not in all_ju2jmh_benchmarks):
                all_ju2jmh_benchmarks.add(ju2jmh_benchmark[0])


    
    grouped_data = {}
    used_benchmarks = set()  # To track which benchmarks have already been grouped
    current_len=0
    current_len_minus_one=0
    counter_current_len=0
    while (len(used_benchmarks) < len(all_ju2jmh_benchmarks)):
        if((len(all_ju2jmh_benchmarks) - len(used_benchmarks)) == current_len):
            counter_current_len +=1
        else:
            current_len = len(all_ju2jmh_benchmarks) - len(used_benchmarks)
            counter_current_len =0
        if(counter_current_len >= 500):
            break

        current_len =len(all_ju2jmh_benchmarks) - len(used_benchmarks)

        for jmh_benchmark, ju2jmh_list in benchmark_data.items():
            # Filter out benchmarks with runtime exceeding the threshold or already grouped
            valid_ju2jmh_list = [
                benchmark for benchmark in ju2jmh_list
                if benchmark[0] not in used_benchmarks
            ]
            if jmh_benchmark not in grouped_data:
                grouped_data[jmh_benchmark] = []

            # Sort ju2jmh benchmarks by similarity score in descending order
            valid_ju2jmh_list.sort(key=lambda x: x[3], reverse=True)
            
            groups = []
            current_group = []
            current_benchmarks = set()
            current_runtime = 0.0
            myFlag=True
            while valid_ju2jmh_list and myFlag:
                # Get the ju2jmh benchmark with the highest similarity score
                ju2jmh_benchmark = valid_ju2jmh_list.pop(0)
                runtime = ju2jmh_benchmark[2]
                if current_runtime + runtime <= threshold:
                    current_group.append(ju2jmh_benchmark)
                    current_runtime += runtime
                    current_benchmarks.add(ju2jmh_benchmark[0])
                    # used_benchmarks.add(ju2jmh_benchmark[0])  # Mark as used
                else:
                    # Finalize the current group and start a new one
                    # print(len(current_benchmarks))
                    if len(current_benchmarks) > 1:
                        # print(current_group)
                        groups.append(current_group)
                        for bench in current_benchmarks:
                            used_benchmarks.add(bench)  # Mark as used    
                        myFlag=False
                    # current_group = [ju2jmh_benchmark]
                    # current_runtime = runtime
                    # used_benchmarks.add(ju2jmh_benchmark[0])  # Mark as used

            # # Add the last group if it's not empty
            # if current_group:
            #     groups.append(current_group)

            if groups:
                grouped_data[jmh_benchmark].append(groups)
    # print(grouped_data)
    return grouped_data

# Function to parse the benchmark data from the input file
def parse_benchmark_data_from_file(file_path: str) -> BenchmarkData:
    benchmark_data: BenchmarkData = {}

    with open(file_path, 'r', encoding='utf-8') as file:
        current_jmh_benchmark = None
        for line in file:
            line = line.strip()
            
            if line.startswith("> JMH Benchmark:"):
                current_jmh_benchmark = line.split(":")[1].strip()
                benchmark_data[current_jmh_benchmark] = []
            elif line and ',' in line:
                parts = line.split(":")
                
                if len(parts) == 4:
                    try:
                        name, score, throughput  = parts[1].split(',')[0].strip(), parts[2].split(',')[0].strip(), parts[3].split(',')[0].strip()
                        throughput = float(throughput)
                        runtime = float(1/throughput) if throughput != "N/A" else 199999.0
                        score = float(score.replace('%',''))
                        benchmark_data[current_jmh_benchmark].append((name, throughput, runtime, score))
                    except ValueError:
                        # If conversion fails (e.g., due to non-numeric value), skip this line
                        continue

    return benchmark_data


# Function to save the output to a text file with only group names
def save_cluster_all_possible_to_file(clusters_all_possible_data: Dict[str, List[List[Ju2JmhBenchmark]]], output_file_path: str):
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for jmh_benchmark, groups in clusters_all_possible_data.items():
            file.write("> JMH Benchmark: "+f"{jmh_benchmark}\n")
            for i, group in enumerate(groups):
                file.write(" Group "+str(i+1)+" : \n")
                for ju2jmh in group:
                    name, _, _, _ = ju2jmh  # Extract only the name of the benchmark
                    file.write(f"{name}\n")
            file.write("\n")

# Function to save the output to a text file with only group names
def save_cluster_highest_overlap_to_file(clusters_highest_overlap_data: Dict[str, List[List[Ju2JmhBenchmark]]], output_file_path: str):
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for jmh_benchmark, groups in clusters_highest_overlap_data.items():
            file.write("> JMH Benchmark: "+f"{jmh_benchmark}\n")
            for i, group in enumerate(groups):
                file.write(" Group "+str(i+1)+" : \n")
                for g in group:
                    for ju2jmh in g:
                        name, _, _, _ = ju2jmh  # Extract only the name of the benchmark
                        file.write(f"{name}\n")
            file.write("\n")

# Function to save the output to a text file with only group names
def save_cluster_ready_to_generate_file(clusters_highest_overlap_data: Dict[str, List[List[Ju2JmhBenchmark]]], output_file_path: str):
    clusters_counter=0
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for jmh_benchmark, groups in clusters_highest_overlap_data.items():
            for i, group in enumerate(groups):
                clusters_counter +=1
                file.write("Cluster_"+str(clusters_counter)+":")
                for g in group:
                    for ju2jmh in g:
                        name, _, _, _ = ju2jmh  # Extract only the name of the benchmark
                        file.write(name + ",")
                file.write("\n")


# Function to save the output to a text file with only group names
def save_clustered_ju2jmh_benchmarks_file(clusters_highest_overlap_data: Dict[str, List[List[Ju2JmhBenchmark]]], output_file_path: str):
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for jmh_benchmark, groups in clusters_highest_overlap_data.items():
            for i, group in enumerate(groups):
                for g in group:
                    for ju2jmh in g:
                        name, _, _, _ = ju2jmh  # Extract only the name of the benchmark
                        file.write(name + "\n")


# Main execution flow
if __name__ == "__main__":
    # input file that the measured overlapping in code coverage from the 'jmh_ju2jmh_overlap_measurement.py' (equal to output_file_path = "jmh_ju2jmh_overlap.txt")
    input_file_path = 'jmh_ju2jmh_overlap.txt'  

    # clusters along with all possible ju2jmh benchmarks that have some overlapping with a JMH benchmark (can be duplicated)
    clusters_all_possible_file = 'results/clusters_all_possible.txt'

    # clusters along with ju2jmh benchmarks that have highest overlapping coverage with a JMH benchmark (non-duplicated)
    clusters_highest_overlap_file = 'results/clusters_highest_overlap.txt'

    # clusters along with ju2jmh benchmarks that have highest overlapping coverage with a JMH benchmark (non-duplicated), and the accumulated throughput is below the threshold
    clusters_ready_to_generate_file = 'results/clusters_ready_to_generate_file.txt'
    # Set the threshold for the cumulative runtime of a group
    runtime_threshold = 0.000005  # 5 microseconds or 0.000005 seconds

    # All ju2jmh benchmarks that are clustered
    clustered_ju2jmh_benchmarks = 'results/clustered_ju2jmh_benchmarks.txt'  

    # Parse the benchmark data from the input file
    benchmark_data = parse_benchmark_data_from_file(input_file_path)

    # Generate groups
    clusters_all_possible_data = clusters_all_possible(benchmark_data, runtime_threshold)
    clusters_highest_overlap_data = clusters_highest_overlap(benchmark_data, runtime_threshold)

    # Save the grouped benchmark names to a file (names only)
    save_cluster_all_possible_to_file(clusters_all_possible_data, clusters_all_possible_file)
    save_cluster_highest_overlap_to_file(clusters_highest_overlap_data, clusters_highest_overlap_file)
    save_cluster_ready_to_generate_file(clusters_highest_overlap_data, clusters_ready_to_generate_file)
    save_clustered_ju2jmh_benchmarks_file(clusters_highest_overlap_data, clustered_ju2jmh_benchmarks)

    # print(f"Group names have been saved to {group_names_output_file_path}")
