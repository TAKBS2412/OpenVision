#!/usr/bin/env python3
#
# A NetworkTables client that performs vision processing constantly and sends the calculated data to the roboRIO

from networktables import NetworkTables

import logging
logging.basicConfig(level=logging.DEBUG)

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import image_proc
import numpy as np
import sys

import image
import image_proc

ip = "10.24.12.105"

NetworkTables.initialize(server=ip)

sd = NetworkTables.getTable("datatable")

imgwpx = 640
imghpx = 480
resolution = (imgwpx, imghpx) 
camera = image.initCamera(resolution)

while True:
	# Do vision processing stuff here
	angle = distance = 0 # Default values
	targetsFound = False
	# The vision processing stuff below will set the above variables
	img = image.takePicture(camera)
	img = image.procImage(img, resolution, 80, 40, 0, 130, 255, 200)
	largestCnt = image.getLargestContour(img)
	if largestCnt is None:
		# No targets found
		targetsFound = False
		print("No targets found!")
	else:
		targetsFound = True
		boundingrect = cv2.minAreaRect(largestCnt)
		wpx, hpx = boundingrect[1]
		viewangle = 0.698
		distance = image_proc.getDistance(imghpx, 5.08, hpx, viewangle)
		angle = image_proc.getHorizAngle(imghpx, 5.08, distance, hpx, image.getContourCentroidCoords(largestCnt)[0])
		print("Angle: " + str(angle))
		print("Distance: " + str(distance))

	# Send the variables to the roboRIO
	sd.putNumber("angle", angle)
	sd.putNumber("distance", distance)
	sd.putBoolean("targetsFound", targetsFound)
