#!/bin/bash

echo "##  Migrate and apply ##"
python3.7 manage.py makemigrations
python3.7 manage.py migrate

