#!/bin/bash
# Runs the experiments, monitoring for failures and restarts
# Must be in smt virtual environment and have done setup_run.sh
# Monitoring interval
DELAY=10800
# Fewer than this multiprocessing tasks forces a restart
COUNT=3

function runit () {
    echo ""
    echo "*** New iteration at: `date` ***"
    echo ""
    bash kill.sh
    python $HOME/home/Technical/smarte/smarte/workunit_runner.py  &
}

# Monitor and restart if necesary
while :
do
    #count=`ps aux | grep "multiprocessing.spawn" | wc | awk '{print $1}'`
    #if (( ${count} < ${COUNT})); then
    #    bash kill.sh
    #    runit
    #fi
    runit
    sleep ${DELAY}
done
