#! /bin/bash
source ~/.profile
workon cv
python nt_client.py 2> ~/error.log
