#!/bin/bash

source bashrc

git clone --depth 1 --branch paper https://gitlab.com/MpiBugsInitiative/MpiBugsInitiative.git mbi

cp tracer/* mbi/scripts/tools

cd mbi/
git apply ../patch/mbi-script.patch

python3 ./MBI.py -c generate

mkdir -p "${MPI_ARG_TRACE_DIR}"


