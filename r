#!/bin/bash
# Runs a test, deleting extraneous output
# $1 - name of source file under test
python tests/test_$1.py 2>&1 | ~/BaseStack/bin/filter_pycapsule.py
