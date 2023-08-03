#!/bin/bash

source ../mpi-arg-tracer/bashrc
source bashrc

cd "$MPI_CORRBENCH_TRACER_EXEC_DIR"

./2Ranks.sh
