#! /bin/bash
source ~/.profile
workon cv

# Ping 10 times
ping 10.24.12.1 -c 10 > /home/pi/src/logs/ping.log

echo "-----------------------" >> /home/pi/src/logs/output.log
python ~/src/nt_client.py >> /home/pi/src/logs/output.log 2>&1
