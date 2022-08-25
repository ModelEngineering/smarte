#!/bin/bash
pyenv exec python -m venv smt
source smt/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
