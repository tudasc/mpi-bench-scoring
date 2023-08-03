# mpi-bench-scoring

Reproducibility setup assessing whether the existing MPI correctness benchmarks, MPI-CorrBench and the MPI Bugs
Initiative, mirror the MPI usage of real-world HPC codes.
Our analysis combines static source text analysis and dynamic MPI call tracing to generate a database for comparison.

## Using the tool chain

To generate our coverage data for each correctness benchmark, we
need to (1) build our PMPI-based interceptor library to trace MPI
usage, (2) modify MPI-CorrBench and (3) MPI Bugs Initiative to execute and analyze
their tests with our tooling to generate the static & dynamic traces, (4) use our
Python-based MPI usage analysis tool to merge the resulting trace
with the statically collected MPI usage database, and execute it
again to generate the final coverage data of the HPC data set.

### 1. Tracing MPI calls: mpi-arg-tracer

The [MPI call tracer](https://github.com/ahueck/mpi-arg-trace/tree/main) is a shared lib that needs to be preloaded
before running the MPI target code.

1. Call [init.sh](mpi-arg-tracer/init.sh) to clone & compile the code.
    * This requires Clang (v12) & llvm-symbolizer and Python3 for the PMPI wrapper
2. Source [bashrc](mpi-arg-tracer/bashrc) to set environment path variables for later steps

### 2. MPI-CorrBench (COBE)

Requires `mpi-arg-tracer` & `mpi-arg-usage` (latter is for static collection in step 2.1)

1. Source [bashrc](mpi-corrbench/bashrc) to set required environment (path) variables
2. Call [init.sh](mpi-corrbench/init.sh) to clone & format the MPI test cases and install the MPI tracer tool.
    * [format.py](mpi-corrbench/format.py) is the formats the code using `clang-format`.
3. Run [execute.sh](mpi-corrbench/execute.sh) to evaluate the benchmark with
   our [MPI tracer](mpi-corrbench/tracer/2Ranks.sh) and generate dynamic MPI usage data.

#### 2.1 Collect static MPI usage

This step is used to generate static MPI usage data (to be merged with the dynamic) one.
It relies only on the `mpi-arg-usage` tool & the benchmarks test sources.

1. Call [collect_static_data.sh](mpi-corrbench/collect_static_data.sh) runs our MPI usage analysis tool `mpi-arg-usage`
   on the test cases.

### 3. MPI Bugs Initiative (MBI)

Requires `mpi-arg-tracer` & `mpi-arg-usage` (latter is for static collection in step 3.1)

1. Source [bashrc](mpi-corrbench/bashrc) to set required environment (path) variables
2. Call [init.sh](mpi-bugs-initiative/init.sh) to clone project and install the MPI tracer tool.
    * [patch file](mpi-bugs-initiative/patch/mbi-script.patch) is applied to
      add [our tracing tool](mpi-bugs-initiative/tracer/mpi_arg_tracer.py) to MBI
3. Run [execute.sh](mpi-corrbench/execute.sh) to evaluate the benchmark with our MPI tracer and generate dynamic MPI
   usage data.

#### 3.1 Collect static MPI usage

This step is used to generate static MPI usage data (to be merged with the dynamic) one.
It relies only on the `mpi-arg-usage` tool & the benchmarks test sources.

1. Call [collect_static_data.sh](mpi-bugs-initiative/collect_static_data.sh) runs our MPI usage analysis
   tool `mpi-arg-usage` on the test cases.

### 4. MPI scoring: mpi-arg-usage

Requires previous steps 1-3.

1. Source [bashrc](mpi-scoring/bashrc) to set required environment (path) variables
2. Call [init.sh](mpi-scoring/init.sh) to clone project and install Python package requirements with conda. 
3. Run [execute.sh](mpi-scoring/execute.sh) to evaluate the benchmarks MPI usage w.r.t. HPC data set.
   * Initializes HPC data set by extracting the existing tar.gz (refer to [mpi-arg-usage](https://github.com/tudasc/mpi-arg-usage/)), 
   * merges static and dynamic data of correctness benchmarks and
   * generates the final plots.

## Continuous integration for artifacts

Our tool chain automatically generates data sets and plots for publishing purposes,
see [CI file](.github/workflows/ci.yml).

For each (successful) run, artifacts are attached,
see [All Workflows](https://github.com/ahueck/mpi-bench-scoring/actions):

- `corrbench-trace`: Dynamic MPI trace of MPI-CorrBench.
- `mbi-trace`: Dynamic MPI trace of MPI Bugs Initiative (with 1s timeout (e.g., deadlocks) to save time).
- `plots`: Visualization of scoring MPI usage patterns w.r.t. the HPC data set.