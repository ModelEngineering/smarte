#!/bin/bash
git clone --recurse-submodules https://github.com/ModelEngineering/smarte.git
git clone --recurse-submodules https://github.com/ModelEngineering/fitterpp.git
git clone --recurse-submodules https://github.com/ModelEngineering/SBMLModel.git
cd smarte
setup_env.sh
