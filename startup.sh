#! /bin/bash
source ~/.profile
workon cv

# Ping 10 times

ping 10.24.12.1 -c 10

echo "-----------------------" >> /home/pi/src/logs/output.log
python nt_client.py >> /home/pi/src/logs/output.log 2>&1
