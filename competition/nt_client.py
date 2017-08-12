#!/usr/bin/env python3
#
# A NetworkTables client that performs vision processing constantly and sends the calculated data to the roboRIO
from __future__ import division
from picamera.array import PiRGBArray
from picamera import PiCamera

import time
import cv2
import image_proc
import numpy as np
import sys

import image
import image_proc
import Constants
import Updater

# Create Constants
constants = Constants.Constants("nt_settings")

updater = Updater.Updater()


rawCapture = PiRGBArray(constants.camera, size=constants.camera.resolution)

# Lower the shutter_speed
constants.camera.shutter_speed = 300

for frame in constants.camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
		
	#img = frame.array
	img = cv2.imread("../waamv/orig2.jpg")
	oldimg = img

	# Do vision processing stuff here
	angle = distance = ratio = 0 # Default values
	targetsFound = pegclose = False
	
	# The vision processing stuff below will set the above variables
	
	# HSV filter the image
	img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	lower_range = np.array([constants.getValue("lowerh"), constants.getValue("lowers"), constants.getValue("lowerv")])
	higher_range = np.array([constants.getValue("higherh"), constants.getValue("highers"), constants.getValue("higherv")])
	HSVmask = cv2.inRange(img, lower_range, higher_range)
	img = cv2.bitwise_and(img, img, mask=HSVmask)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	
	# Process the image	
	contours = image.getSecondLargestContour(img)
	if contours is None:
		# No targets found
		targetsFound = False
		print("No targets found!")
		if not constants.getValue("imagesaved"):
			cv2.imwrite("no-targets-found.jpg", oldimg)
			cv2.imwrite("no-targets-found_proc.jpg", img)
			constants.setValue("imagesaved", True)
		# Clear the stream for the next frame
		rawCapture.truncate(0)
		continue
	largestCnt, secondLargestCnt = contours
	if largestCnt is None or secondLargestCnt is None:
		# Invalid contours
		targetsFound = False
		print("Invalid contours!")
		if not constants.getValue("imagesaved"):
			cv2.imwrite("invalid-contours.jpg", oldimg)
			cv2.imwrite("invalid-contours-proc.jpg", img)
			constants.setValue("imagesaved", True)
		# Clear the stream for the next frame
		rawCapture.truncate(0)
		continue

	targetsFound = True
	_x, _y, wpx, hpx = cv2.boundingRect(largestCnt)
	ratio = hpx/wpx
	viewangle = 0.726
			
	# Find the centroid's coordinates
	cntcoords = image.getContourCentroidCoords(largestCnt)
	cnt2coords = image.getContourCentroidCoords(secondLargestCnt)
	if cntcoords is None or cnt2coords is None:
		pass
	else:
		cx, cy = cntcoords
		cx2, cy2 = cnt2coords
		pegx = (cx + cx2) / 2 # Find the x-coord of the peg (the average of the x-coordinates of the two vision targets)
				
		distance = image_proc.getDistance(constants.getValue("imghpx"), 5.08, hpx, viewangle)
		angle = image_proc.getHorizAngle(constants.getValue("imgwpx"), 5.08, distance, hpx, pegx)
		pegclose = ratio < 2
		
		print("Ratio: " + str(ratio))
		print("Angle: " + str(angle))
		print("Distance: " + str(distance))
		print("Peg close: " + str(pegclose))
		if pegclose and not constants.getValue("imagesaved"):
			cv2.imwrite("pegclose.jpg", oldimg)
			cv2.imwrite("pegclose-proc.jpg", img)
			constants.setValue("imagesaved", True)
	updater.sendData(constants.sd, angle, distance, pegclose, targetsFound)
		
	# Clear the stream for the next frame
	rawCapture.truncate(0)
