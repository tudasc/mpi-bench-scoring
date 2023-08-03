#!/bin/bash

git clone --depth 1 https://github.com/ahueck/mpi-arg-trace.git
cd mpi-arg-trace/

CC=clang CXX=clang++ cmake -B build -DCMAKE_BUILD_TYPE=Release

cmake --build build --target mpitracer_mpitracer
