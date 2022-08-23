#!/bin/bash
# Runs the experiments for 30 min intervals
# Must be in smt virtual environment and have done setup_run.sh
while :
do
    python smarte/experiment_runner.py & 
    sleep 1800
    PID=`ps aux | grep "experiment_runner" | grep -v "grep" \
          | awk '{print $2}'`
    kill -9 ${PID}
done
