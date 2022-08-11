#!/bin/bash
git clone --recurse-submodules https://github.com/ModelEngineering/smarte.git
cd smarte
pip install -r requirements.txt
nosetests tests
