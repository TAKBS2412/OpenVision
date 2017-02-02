#!/usr/bin/env python3

import sys
import time
from networktables import NetworkTables

import logging
logging.basicConfig(level=logging.DEBUG)

from picamera import PiCamera
from picamera import PiRGBArray
import image

ip = "10.24.12.105"

NetworkTables.initialize(server=ip)

camera = PiCamera()


def valueChanged(table, key, value, isNew):
	print("valueChanged: key: '%s'; value: %s; isNew: %s" % (key, vaue, isNew))
	# Send image data back to the roboRIO
	capture = image.takePicture(camera)
	table.putRaw("Image", capture)
	
def connectionListener(connected, info):
	print(info, '; Connected=%s' % connected)

NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)

sd = NetworkTables.getTable("datatable")
sd.addTableListener(valueChanged)

while True:
	time.sleep(1)	
