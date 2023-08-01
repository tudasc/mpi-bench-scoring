#!/bin/bash

source bashrc

git clone --depth 1 --branch v1.2.1 https://github.com/tudasc/MPI-Corrbench.git mpi-corrbench

python3 format.py mpi-corrbench/micro-benches/0-level

cp -R tracer mpi-corrbench/scripts/

mkdir -p "${MPI_ARG_TRACE_DIR}"
