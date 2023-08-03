#!/bin/bash

source bashrc

git clone --depth 1 --branch v1.2.1 https://github.com/tudasc/MPI-Corrbench.git

python3 format.py MPI-Corrbench/micro-benches/0-level

cp -R tracer MPI-Corrbench/scripts/

mkdir -p "${MPI_ARG_TRACE_DIR}"
