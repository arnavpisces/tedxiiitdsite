#!/bin/bash
python createflashsale.py $1
systemctl restart flaskapp
