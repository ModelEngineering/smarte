#!/bin/bash
# Runs the experiments for 30min intervals
# Must be in smt virtual environment and have done setup_run.sh
while :
do
    echo ""
    echo "*** New iteration at: `date` ***"
    echo ""
    python smarte/experiment_runner.py  &
    sleep 1800
    bash kill.sh
done
