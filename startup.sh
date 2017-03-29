#! /bin/bash
source ~/.profile
workon cv
echo "-----------------------" >> /home/pi/src/logs/output.log
python nt_client.py >> /home/pi/src/logs/output.log 2>&1
