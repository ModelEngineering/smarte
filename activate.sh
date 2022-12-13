#!/bin/bash
deactivate
export PYTHONPATH=`pwd`:../fitterpp/:../SBMLModel/:$PYTHONPATH
source smt/bin/activate
