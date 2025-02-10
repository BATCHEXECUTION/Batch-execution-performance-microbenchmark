## Overview
This folder contains two scripts designed for analyzing the code coverage of Java Microbenchmark Harness (JMH) and JUnit-to-JMH (ju2jmh) benchmarks. The first script measures the code coverage of each JMH/ju2jmh benchmark individually, while the second script processes JaCoCo XML reports and extracts only the covered lines into a CSV format.

## Scripts

### 1. Benchmark Coverage Measurement Script (`measure_coverage.sh`)
This Bash script runs JMH/ju2jmh benchmarks individually and measures their code coverage using JaCoCo. It ensures that all required dependencies exist, executes the benchmarks with JaCoCo instrumentation, and generates coverage reports in XML format. The script then converts the XML reports to CSV for further analysis.

#### Dependencies
- Java
- JaCoCo agent and CLI JAR files
- JMH/ju2jmh benchmark JAR file
- A list of JMH/ju2jmh benchmarks (stored in `benchmark_list.txt`)
- Python3 (for post-processing)

#### Usage
```bash
chmod +x measure_coverage.sh
./measure_coverage.sh
```
Ensure that all paths (such as `JMH_JAR_FILE`, `JACOCO_AGENT_JAR`, etc.) are correctly configured in the script.

### 2. XML to CSV Coverage Extraction Script (`jacoco_xml_to_csv_only_covered_lines.py`)
This Python script processes a JaCoCo XML coverage report and extracts only the covered lines (i.e., lines with execution count greater than zero). The output is saved in CSV format for easier analysis.

#### Dependencies
- Python 3
- XML and CSV handling libraries (`xml.etree.ElementTree`, `csv`, `sys`, `re`)

#### Usage
```bash
python3 jacoco_xml_to_csv_only_covered_lines.py <input_jacoco_xml_report> <output_extracted_data.csv>
```

## Output
- The `measure_coverage.sh` script generates per-benchmark coverage reports in an output directory.
- The Python script extracts covered lines from XML reports and saves them in a structured CSV format.

