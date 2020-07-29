#!/bin/bash

echo "##  Running Back Server  ##"
source .env/bin/activate
python3.7 manage.py process_tasks

