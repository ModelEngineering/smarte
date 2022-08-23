#!/bin/bash
# Runs the experiments for 45 min intervals
# Must be in smt virtual environment and have done setup_run.sh
while :
do
    echo ""
    echo "*** New iteration at: `date` ***"
    echo ""
    python smarte/experiment_runner.py & 
    sleep 2700
    bash kill.sh
done
