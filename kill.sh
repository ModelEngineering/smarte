#!/bin/bash
# Kills the computation
PID=`ps aux | grep "workunit_runner" | grep -v "grep" \
      | awk '{print $2}'`
kill -9 ${PID}
