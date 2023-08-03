#!/bin/bash

source bashrc

git clone --depth 1 --branch paper https://gitlab.com/MpiBugsInitiative/MpiBugsInitiative.git

# we do not want to analyze the tools/sourcecode and or execution themselve
rm -rf MpiBugsInitiative/tools

cp tracer/* MpiBugsInitiative/scripts/tools

cd MpiBugsInitiative/
git apply ../patch/mbi-script.patch

python3 ./MBI.py -c generate

mkdir -p "${MPI_ARG_TRACE_DIR}"


