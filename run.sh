#!/bin/bash
# Runs the experiments specified in experiments/workunits.txt
# Must be in smt virtual environment and have done setup_run.sh

for w in `cat experiments/workunits.txt`
  do
    python smarte/workunit_runner.py $w &
  done
