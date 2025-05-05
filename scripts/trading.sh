#!/bin/bash
export PYTHONPATH=$SOL_PROJECT_PATH:$PYTHONPATH

cd $SOL_PROJECT_PATH
source venv/bin/activate
python3 wallet/trading.py
