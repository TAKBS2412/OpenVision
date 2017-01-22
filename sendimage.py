#!/usr/bin/env python3

import sys
import time
from networktables import NetworkTables

import logging
logging.basicConfig(level=logging.DEBUG)

ip = "10.24.12.105"

NetworkTables.initialize(server=ip)

def valueChanged(table, key, value, isNew):
	print("valueChanged: key: '%s'; value: %s; isNew: %s" % (key, vaue, isNew))
	
def connectionListener(connected, info):
	print(info, '; Connected=%s' % connected)

NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)

sd = NetworkTables.getTable("datatable")
sd.addTableListener(valueChanged)

while True:
	time.sleep(1)	
