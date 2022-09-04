#!/bin/bash
# Counts the number of simulations completed
#ls -lh *.csv | awk '{print $5}' | sed 's/K//'  | sed 's/M/000/' | \
#   paste -sd+ - | sed 's/++/+/g' | sed 's/+$//' | bc
grep -v "biomodel" *10000*.csv | wc | awk '{print $2}'
for f in *.csv
   do
    echo $f `cat $f | wc | awk '{print $2-1}'`
   done
