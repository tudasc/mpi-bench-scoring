#!/bin/bash

source ../mpi-scoring/bashrc
source bashrc

source activate $ENV_NAME

# collect the static data

cd $MPI_ARG_USAGE_BASE 

# set up code locations file
echo "Code,Language,Type,URL,Comment,SHA" > src_location.csv
echo "MpiBugsInitiative,C,git,https://gitlab.com/MpiBugsInitiative/MpiBugsInitiative.git,,4ec1c8c4e66b264ebe44d74cbd9c353dcbd6b876" >> src_location.csv


python3 mpi_usage_analysis.py --output $MPI_ARG_TRACE_DIR/MBI-Static.csv --code_locations src_location.csv --repo_path $MBI_BASE/..
