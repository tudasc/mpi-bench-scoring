#!/bin/bash

source ../mpi-arg-tracer/bashrc
source bashrc

cd "$MBI_TRACER_EXEC_DIR"

if [[ $CI_SCORE_TEST == 1 ]]; then
  mv gencodes gencodes-all
  mkdir gencodes
  cp gencodes-all/CallParamCorrect_Comm_create.c gencodes/
fi

python3 ./MBI.py -x arg-tracer -t 1 -c run

