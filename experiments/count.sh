#!/bin/bash
# Counts the number of simulations completed
#ls -lh *.csv | awk '{print $5}' | sed 's/K//'  | sed 's/M/000/' | \
#   paste -sd+ - | sed 's/++/+/g' | sed 's/+$//' | bc
grep -v "biomodel" *.csv | wc | awk '{print $2}'
