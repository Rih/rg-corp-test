#!/bin/bash

echo "##  Running Back Server  ##"
source .env/bin/activate
python manage.py runserver

