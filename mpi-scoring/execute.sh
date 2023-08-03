#!/bin/bash

source bashrc

source activate $ENV_NAME

# the output contains one file per process but we consider it all together

cat $COBE_FILES/mpi-arg-trace-*.csv > $COBE_FILES/cobe_dynamic.csv
cat $MBI_FILES/mpi-arg-trace-*.csv > $MBI_FILES/mbi_dynamic.csv

# the full hpc applications dataset to score against
tar -xzf $HPC_DATA_DIR/output.csv.tar.gz -C $HPC_DATA_DIR

cd $MPI_ARG_USAGE_BASE 

# merge static and dynamic data
python3 merge_dynamic_data.py --output $MBI_FILES/merged_mbi.csv --input_static $MBI_FILES/MBI-Static.csv --input_dynamic $MBI_FILES/mbi_dynamic.csv
python3 merge_dynamic_data.py --output $COBE_FILES/merged_cobe.csv --input_static $COBE_FILES/Cobe-Static.csv --input_dynamic $COBE_FILES/cobe_dynamic.csv

# perform the scoring and generate the plots
python3 score_corbenchs.py --input $HPC_DATA_DIR/output.csv --cobe $COBE_FILES/merged_cobe.csv --mbi $MBI_FILES/merged_mbi.csv

# move result plots to their own dir
mkdir plots

mv *.pdf plots
