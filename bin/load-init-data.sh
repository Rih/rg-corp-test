#!/bin/bash

echo "##  LOAD ALL FIXTURES  ##"
echo "[+] Scraper"
python3.7 manage.py loaddata scraper.json

