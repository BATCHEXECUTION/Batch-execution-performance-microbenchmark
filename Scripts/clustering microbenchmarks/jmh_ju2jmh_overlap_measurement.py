import os
import csv
from typing import Dict, List

# Type aliases for better readability
CoverageData = Dict[str, Dict[str, List[int]]]
ThroughputData = Dict[str, float]  # Maps JU2JMH benchmark names to their throughput values

def main() -> None:
    """
    Main function to generate and save a summary report of JMH benchmarks and their
    associated JU2JMH benchmarks with coverage >= 10%, sorted by overlap percentage,
    including throughput from ju2jmh.csv.
    """
    # Directory containing individual coverage reports folder. (equal to OUTPUT_DIR="output_directory" in measure_coverage.sh)
    folder_path = "path_to_individual_coverage_report"

    # Path to the ju2jmh benchmark throughputs. The file should include all benchmarks' name along with a single throughput data for each.
    throughput_file = "path_to_ju2jmh_throughput_results.csv"

    # Output file path. This file will include all JMH benchmarks, and for each JMH benchmark, all ju2jmh benchmarks that have some overlapping coverage.
    output_file_path = "jmh_ju2jmh_overlap.txt"
    

    # Load throughput data
    throughput_data = load_throughput_data(throughput_file)
    # Generate the report and save it to a file
    generate_summary_report(folder_path, throughput_data, output_file_path)

def load_throughput_data(file_path: str) -> ThroughputData:
    """
    Loads throughput data from the given CSV file.

    Args:
        file_path: Path to the ju2jmh.csv file.

    Returns:
        A dictionary mapping JU2JMH benchmark names to their throughput values.
    """
    throughput_data: ThroughputData = {}
    try:
        with open(file_path, newline='', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            # Skip the header row
            next(csv_reader, None)
            for row in csv_reader:
                if len(row) < 2:
                    continue  # Skip invalid rows
                benchmark_name, throughput = row[0], row[1]
                try:
                    throughput_data[benchmark_name] = float(throughput)
                except ValueError:
                    print(f"Warning: Invalid throughput value for {benchmark_name}: {throughput}")
    except FileNotFoundError:
        print(f"Error: Throughput file {file_path} not found.")
    except Exception as e:
        print(f"Error reading throughput data: {e}")
    return throughput_data

def generate_summary_report(folder_path: str, throughput_data: ThroughputData, output_file_path: str) -> None:
    """
    Saves a summary report of JMH benchmarks and their associated JU2JMH benchmarks
    with coverage >= 10%, sorted by overlap percentage, including throughput.

    Args:
        folder_path: Path to the folder containing coverage reports.
        throughput_data: A dictionary of throughput values for JU2JMH benchmarks.
        output_file_path: Path to the output file where the report will be saved.
    """
    # Get all benchmark folders
    benchmark_folders = [
        f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))
    ]

    # Separate JMH and JU2JMH benchmarks
    jmh_benchmarks = [
        f for f in benchmark_folders if "_Benchmark.benchmark_" not in f
    ]
    ju2jmh_benchmarks = [
        f for f in benchmark_folders if "_Benchmark.benchmark_" in f
    ]

    # Open the output file for writing
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        # Compare each JMH benchmark with all JU2JMH benchmarks
        for jmh_folder in jmh_benchmarks:
            jmh_path = os.path.join(folder_path, jmh_folder)
            jmh_coverage = get_coverage_data(jmh_path)

            matched_ju2jmh = []

            for ju2jmh_folder in ju2jmh_benchmarks:
                ju2jmh_path = os.path.join(folder_path, ju2jmh_folder)
                ju2jmh_coverage = get_coverage_data(ju2jmh_path)

                # Calculate overlap
                intersection = calculate_intersection_coverage(jmh_coverage, ju2jmh_coverage)
                total_lines_ju2jmh = sum(
                    len(lines)
                    for classes in ju2jmh_coverage.values()
                    for lines in classes.values()
                )
                total_common_lines = sum(
                    len(lines)
                    for classes in intersection.values()
                    for lines in classes.values()
                )
                overlap_percentage = (
                    (total_common_lines / total_lines_ju2jmh) * 100
                    if total_lines_ju2jmh
                    else 0
                )

                # Filter for coverage >= 10%
                if overlap_percentage >= 0:
                    matched_ju2jmh.append((ju2jmh_folder, overlap_percentage))

            # Sort matches by overlap percentage in descending order
            matched_ju2jmh.sort(key=lambda x: x[1], reverse=True)

            if matched_ju2jmh:
                output_file.write(f"> JMH Benchmark: {jmh_folder}\n")
                for ju2jmh_folder, overlap in matched_ju2jmh:
                    throughput = throughput_data.get(ju2jmh_folder, "N/A")
                    output_file.write(f" >> JU2JMH Benchmark: {ju2jmh_folder}, Overlap: {overlap:.2f}%, Throughput: {throughput}\n")
                output_file.write("\n")

def get_coverage_data(directory: str) -> CoverageData:
    """
    Reads and parses coverage data from a CSV file in the given directory.

    Args:
        directory: The path to the directory containing the "report.csv" file.

    Returns:
        A dictionary representing the coverage data.
    """
    coverage_data: CoverageData = {}
    csv_file_path = os.path.join(directory, "report.csv")

    try:
        with open(csv_file_path, newline='', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            # Skip the header row
            next(csv_reader, None)

            for row in csv_reader:
                # Each row contains package name, class name, and covered lines.
                if len(row) < 3:
                    continue  # Skip invalid rows

                package_name, class_name, lines_str = row[0], row[1], row[2]
                if lines_str:
                    lines_covered = [int(line.strip()) for line in lines_str.split(";") if line.strip()]
                else:
                    lines_covered = []  # Default to an empty list if lines_str is invalid.

                # Organize data into a nested dictionary structure.
                coverage_data.setdefault(package_name, {}).setdefault(class_name, []).extend(lines_covered)

    except FileNotFoundError:
        print(f"Warning: Coverage report not found in {directory}.")
    except Exception as e:
        print(f"Error reading coverage data from {directory}: {e}")

    return coverage_data

def calculate_intersection_coverage(data1: CoverageData, data2: CoverageData) -> CoverageData:
    """
    Calculates the intersection of coverage data between two benchmarks.

    Args:
        data1: Coverage data from the first benchmark.
        data2: Coverage data from the second benchmark.

    Returns:
        A dictionary containing the intersected coverage data.
    """
    intersection: CoverageData = {}

    for package_name, classes1 in data1.items():
        if package_name in data2:  # Check if the package exists in both datasets.
            for class_name, lines1 in classes1.items():
                if class_name in data2[package_name]:  # Check if the class exists in both datasets.
                    lines2 = data2[package_name][class_name]
                    # Find common lines covered by both datasets.
                    common_lines = [line for line in lines1 if line in lines2]
                    if common_lines:
                        intersection.setdefault(package_name, {}).setdefault(class_name, []).extend(common_lines)

    return intersection

if __name__ == "__main__":
    # Entry point of the script.
    main()