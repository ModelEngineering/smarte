#!/bin/bash
# Eliminates conflict markers from CSV file
cp $1 /tmp
grep "," $1 > $1.sav
cp $1.sav $1
