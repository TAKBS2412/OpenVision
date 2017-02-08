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

rawCapture = PiRGBArray(camera, size=resolution)

# HSV Values to filter
lowerh = 50
lowers = 235
lowerv = 30 #8 for red raspberry pi

higherh = 65
highers = 255
higherv = 80 # 45 for red raspberry pi

# Lower the shutter_speed
camera.shutter_speed = 200

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
		
	img = frame.array

	# Do vision processing stuff here
	angle = distance = 0 # Default values
	targetsFound = False
	
	# The vision processing stuff below will set the above variables
	img = image.procImage(img, lowerh, lowers, lowerv, higherh, highers, higherv)
	largestCnt = secondLargestCnt = None
	contours = image.getSecondLargestContour(img)
	if contours is not None: largestCnt, secondLargestCnt = contours
	if largestCnt is None or secondLargestCnt is None:
		# No targets found
		targetsFound = False
		print("No targets found!")
	else:
		targetsFound = True
		boundingrect = cv2.minAreaRect(largestCnt)
		wpx = max(boundingrect[1])
		hpx = min(boundingrect[1])
		
		viewangle = 0.726
		
		# Find the centroid's coordinates
		cx, cy = image.getContourCentroidCoords(largestCnt)
		cx2, cy2 = image.getContourCentroidCoords(secondLargestCnt)
		pegx = (cx + cx2) / 2 # Find the x-coord of the peg (the average of the x-coordinates of the two vision targets)
		
		distance = image_proc.getDistance(imghpx, 5.08, hpx, viewangle)
		angle = image_proc.getHorizAngle(imgwpx, 5.08, distance, hpx, pegx)
		print("Angle: " + str(angle))
		print("Distance: " + str(distance))

	# Send the variables to the roboRIO
	sd.putNumber("angle", angle)
	sd.putNumber("distance", distance)
	sd.putBoolean("targetsFound", targetsFound)

	# Clear the stream for the next frame
	rawCapture.truncate(0)
