#!/bin/bash

source bashrc

# the output contains one file per process bot we consider it all together

cat $COBE_FILES/mpi-arg-trace-*.csv $COBE_FILES/cobe_dynamic.csv
cat $MBI_FILES/mpi-arg-trace-*.csv $MBI_FILES/mbi_dynamic.csv

# the collected static data for the corrbenchs
tar -xzf mpi-arg-usage/output/MPI-Corrbench.csv.tar.gz $HPC_DATA_DIR
tar -xzf mpi-arg-usage/output/MpiBugsInitiative.csv.tar.gz $HPC_DATA_DIR

# the full hpc applications dataset to score against
tar -xzf mpi-arg-usage/output/output.csv.tar.gz $HPC_DATA_DIR


#TODO run execution
