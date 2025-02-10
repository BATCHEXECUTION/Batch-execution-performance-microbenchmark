Batch execution of performance microbenchmark

This project is a replication package for the paper titled **"Batch Execution of Microbenchmarks for Efficient Performance Testing"** The paper proposes a novel approach to optimize the execution of microbenchmarks, focusing on the grouping of benchmarks with similar code coverage to reduce execution overhead and mitigate the bias introduced by excessively short benchmarks.

---

## **Purpose**

The goal of this project is to provide tools and scripts for automating the process of benchmarking optimization through clustering strategies. These tools facilitate the analysis of the execution time and stability of microbenchmarks across various Java projects by grouping benchmarks with overlapping code coverage.

---

## **Folders Overview**

### **Data**
Contains data files for each three subjects, including throughput results for both set of individual benchmarks and clustered benchmarks.

### **Scripts**
Includes Python and Bash scripts for:
- Analyzing and generating reports on code coverage using JaCoCo.
- Clustering microbenchmarks based on code coverage.
- Generating source code for clustered benchmarks and measuring code coverage overlaps.

---
