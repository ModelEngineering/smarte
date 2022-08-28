#!/bin/bash
# Counts the Kbytes in .csv files
ls -lh *.csv | awk '{print $5}' | sed 's/K//'  | sed 's/M/000/' | \
   paste -sd+ - | sed 's/++/+/g' | sed 's/+$//' | bc
