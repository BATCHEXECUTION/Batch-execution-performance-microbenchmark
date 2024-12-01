
# Batch Execution of Microbenchmarks for Efficient Performance Testing

This repository provides the replication package for the paper titled **"Batch Execution of Microbenchmarks for Efficient Performance Testing."** It includes experimental data and scripts for reproducing the results presented in the paper.

---

## Repository Overview

The replication package consists of scripts and data organized into the following directories:
- **`Scripts`**: Contains scripts for performing various tasks, such as code coverage analysis, similarity measurements and microbenchmark clustering, and evaluation.
- **`Data`**: Includes experimental results and datasets used in the study.

---

## Scripts Overview

The `Scripts` directory contains three subdirectories, each addressing a specific aspect of the experimentation process:

1. **[Code Coverage](#1-code-coverage)**: Scripts for measuring code coverage of microbenchmarks.
2. **[Similarity Measurements and Clustering Microbenchmarks](#2-similarity-measurements-and-clustering-microbenchmarks)**: Scripts for calculating similarity between microbenchmarks and then clustering microbenchmarks based on measured similarity metrics.
3. **[Evaluation](#4-evaluation)**: Scripts for evaluating the performance and efficiency of clustered microbenchmarks.

---

### 1. Code Coverage

This subdirectory contains scripts for measuring the code coverage of handcrafted JMH microbenchmarks and automatically generated `ju2jmh` microbenchmarks. The coverage is measured using the JaCoCo agent, which generates `.exec` files for each microbenchmark execution. These files are processed using the JaCoCo CLI to produce XML reports, which are then converted into CSV files listing all covered lines (organized by package and class).

#### Workflow:
1. **Execution**:
   - The JaCoCo agent collects coverage data during the execution of each microbenchmark.
   - For each microbenchmark, an output folder is created containing:
     - A coverage `.exec` file.
     - A CSV file listing all covered code lines for the microbenchmark.

2. **Output**:
   - Each microbenchmark has its own folder named after the benchmark.
   - Inside each folder, a CSV report lists the covered lines for that specific microbenchmark.

#### Steps to Run the Scripts:
1. Configure the variables in `code_coverage.sh`:
   - `JMH_JAR_FILE`: Path to the JAR file containing the JMH benchmarks.
   - `BENCHMARK_LIST`: Path to the file listing the microbenchmarks.
   - `OUTPUT_DIR`: Output directory for coverage reports.
   - `JACOCO_AGENT_JAR`: Path to the JaCoCo agent JAR file.
   - `JACOCO_CLI_JAR`: Path to the JaCoCo CLI JAR file.
   - `CLASS_FILES`: Path to the compiled classes for coverage analysis.
   - `PYTHON_SCRIPT`: Path to the script for converting XML to CSV.

2. Execute the script using the command:
   ```bash
   sh code_coverage.sh
   ```

---

### 2. Similarity Measurements and Clustering Microbenchmarks

This subdirectory contains scripts to compute similarity metrics between microbenchmarks. These metrics form the basis for clustering microbenchmarks into groups.

#### Workflow:
- Similarity is calculated by comparing the coverage and execution profiles of microbenchmarks.
- Results are stored in a format suitable for clustering.

---

### 3. Evaluation

This subdirectory includes scripts for evaluating the effectiveness and efficiency of the clustering approach. 

#### Metrics:
- **Execution Time**: Reduction in total execution time compared to running benchmarks individually.
- **Resource Utilization**: Efficient use of computational resources.
- **Reliability**: Ensures results from clustered benchmarks are consistent with individual execution.

#### Workflow:
- Runs clustered microbenchmarks and compares results with individual executions.

---

Feel free to explore each directory for more details about the scripts and their usage. If you encounter any issues, refer to the documentation within each script or the paper for additional guidance.
