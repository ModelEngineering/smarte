#!/bin/bash
# Kills the computation
PID=`ps aux | grep "experiment_runner" | grep -v "grep" \
      | awk '{print $2}'`
kill -9 ${PID}
