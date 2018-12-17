#! /bin/bash
source ~/.profile
workon cv

# Ping 10 times
ping 10.24.12.1 -c 10 > /home/pi/src/logs/ping.log

echo "---`date`---" >> /home/pi/src/logs/output.log
python ~/src/competition/main.py ~/src/competition/fast_settings >> /home/pi/src/logs/output.log 2>&1
