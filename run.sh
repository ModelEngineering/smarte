#!/bin/bash
# Runs the experiments for 2hr intervals
# Must be in smt virtual environment and have done setup_run.sh
while :
do
    echo ""
    echo "*** New iteration at: `date` ***"
    echo ""
    python smarte/experiment_runner.py  &
    sleep 7200
    bash kill.sh
done
