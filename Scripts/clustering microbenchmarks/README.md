# Clustering individual ju2jmh benchmarks

This repository includes three Python scripts that assist in analyzing, organizing, and generating source code for JMH and ju2jmh benchmarks. Below is an overview of the scripts and their functionalities.


## 1. `jmh_ju2jmh_overlap_measurement.py`

### Purpose:
This script calculates the overlap in code coverage between JMH benchmarks and ju2jmh benchmarks.

### Functionality:
- It compares the code coverage between each JMH benchmark and each ju2jmh benchmark.
- It outputs a report that shows the percentage overlap between the two sets of benchmarks.


## 2. `clusters_in_a_text.py`

### Purpose:
This script is used to generate a text file that contains a list of clusters and the ju2jmh benchmarks associated with each cluster.

### Functionality:
- It reads the benchmark data, identifies clusters, and maps the ju2jmh benchmarks that belong to each cluster.
- The output is a formatted text file, listing each cluster and the corresponding benchmarks.



## 3. `generate_clusters_source_code.py`

### Purpose:
This script generates source code for benchmark clusters.

### Functionality:
- It generates a Java class for each benchmark cluster, based on the cluster data.
- The generated class includes benchmark methods, field declarations, and setup logic, as well as the necessary calls for running the benchmarks.


## Requirements:
- Python 3.x
- Required Python packages for file handling, text parsing, and other dependencies (e.g., `os`, `glob`).


### Usage:

To use any of these scripts, simply run the script from the command line, and ensure that the input files (e.g., benchmark data, cluster information) are available in the same directory or provide the correct file paths as needed.

