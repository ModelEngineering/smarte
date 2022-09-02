#!/bin/bash
# Runs the experiments, monitoring for failures and restarts
# Must be in smt virtual environment and have done setup_run.sh
DELAY=300
COUNT=3

function runit () {
    echo ""
    echo "*** New iteration at: `date` ***"
    echo ""
    python smarte/experiment_runner.py  &
}

# Monitor and restart if necesary
while :
do
    count=`ps aux | grep "multiprocessing.spawn" | wc | awk '{print $1}'`
    if (( ${count} < ${COUNT})); then
        runit
    fi
    sleep ${DELAY}
done
