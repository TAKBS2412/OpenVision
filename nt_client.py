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

ip = "10.24.12.2"

NetworkTables.initialize(server=ip)

sd = NetworkTables.getTable("datatable")

imgwpx = 640
imghpx = 480
resolution = (imgwpx, imghpx) 
camera = image.initCamera(resolution)

rawCapture = PiRGBArray(camera, size=resolution)

# Lower the shutter_speed
camera.shutter_speed = 300

# If we've already saved an image
imagesaved = False

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
		
	img = frame.array
	oldimg = img

	# Do vision processing stuff here
	angle = distance = ratio = 0 # Default values
	targetsFound = False
	
	# The vision processing stuff below will set the above variables
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	thresh = cv2.threshold(img, 20, 255, cv2.THRESH_BINARY)
	if thresh is not None:
		ret, img = thresh
		contours = image.getSecondLargestContour(img)
		if contours is not None: largestCnt, secondLargestCnt = contours
		if largestCnt is None or secondLargestCnt is None:
			# No targets found
			targetsFound = False
			print("No targets found!")
			if not imagesaved:
				cv2.imwrite("no-targets-found.jpg", oldimg)
				cv2.imwrite("no-targets-found_proc.jpg", img)
				imagesaved = True
		else:
			targetsFound = True
			boundingrect = cv2.minAreaRect(largestCnt)
			wpx = max(boundingrect[1])
			hpx = min(boundingrect[1])
			ratio = wpx/hpx
			viewangle = 0.726
			
			# Find the centroid's coordinates
			cntcoords = image.getContourCentroidCoords(largestCnt)
			cnt2coords = image.getContourCentroidCoords(secondLargestCnt)
			if cntcoords is None or cnt2coords is None:
				print("Invalid contours!")
				targetsFound = False
				if not imagesaved:
					cv2.imwrite("invalid-contours.jpg", oldimg)
					cv2.imwrite("invalid-contours-proc.jpg", img)
					imagesaved = True
			else:
				cx, cy = cntcoords
				cx2, cy2 = cnt2coords
				pegx = (cx + cx2) / 2 # Find the x-coord of the peg (the average of the x-coordinates of the two vision targets)
				
				distance = image_proc.getDistance(imghpx, 5.08, hpx, viewangle)
				angle = image_proc.getHorizAngle(imgwpx, 5.08, distance, hpx, pegx)
				pegclose = ratio < 2
				print("Angle: " + str(angle))
				print("Distance: " + str(distance))
				print("Peg close: " + str(pegclose))
				if pegclose and not imagesaved:
					cv2.imwrite("pegclose.jpg", oldimg)
					cv2.imwrite("pegclose-proc.jpg", img)
					imagesaved = True
	# Send the variables to the roboRIO
	sd.putNumber("angle", angle)
	sd.putNumber("distance", distance)
	sd.putBoolean("pegclose", pegclose) 
	sd.putBoolean("targetsFound", targetsFound)
	
	# Clear the stream for the next frame
	rawCapture.truncate(0)
