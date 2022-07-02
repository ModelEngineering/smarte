#!/bin/bash
# Runs a test, deleting extraneous output
# $1 - name of source file under test
python tests/test_$1.py 2> /tmp/r.out
grep -v "Object of type" /tmp/r.out | \
  grep -v "Exception ignored" | \
  grep -v "PyCapsule" | \
  grep -v "Traceback (most recent" | \
  grep -v "_callTestMethod"  | \
  grep -v "No version"  | \
  grep -v " method()$"
