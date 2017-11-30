# Import libraries
from __future__ import division
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import image # Custom library
import image_proc # Another custom library
import Constants # Yet another custom library
import ImageFiltering # Yet another custom library
import ImageProc # Yet another custom library
import TargetProc # Yet another custom library
import Updater # Yet another custom library
import KeyUpdater
import numpy as np
import datetime

#import points

# Create Constants
constants = Constants.Constants("/home/pi/src/competition/settings")

# Create ImageFiltering
imagefilter = ImageFiltering.ImageFiltering()

# Create ImageProc
imageproc = ImageProc.ImageProc()

# Create TargetProc
targetproc = TargetProc.TargetProc()

# Create Updater
updater = Updater.Updater()

# Create KeyUpdater
keyupdater = KeyUpdater.KeyUpdater()

# Let the camera warm up
time.sleep(0.1)

rawCapture = PiRGBArray(constants.camera, size=constants.camera.resolution)

# Lower the shutter_speed
constants.camera.shutter_speed = 300
	
# Capture and display frames from camera
for frame in constants.camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):	
	# Break from loop if needed.
	if constants.getValue("endloop"):
		break
	
	# Get the currently pressed key if useGUI is enabled.
	if constants.getValue("useGUI"):
		key = cv2.waitKey(1)

	# Grab array representing image
	if constants.getValue("usevideo"):
		img = frame.array
	else:
		img = cv2.imread(constants.getValue("images")[constants.getValue("index")])

	oldimg = img

	oldtime = datetime.datetime.now()
	img = imagefilter.filterImage(img, constants)
	elapsedtime = datetime.datetime.now() - oldtime
	print("ImageFiltering - Time elapsed (s): " + str(elapsedtime.microseconds/1000000.0))
	
	if constants.getValue("procImage"):
		oldtime = datetime.datetime.now()
		contours = imageproc.procImage(img, constants)
		elapsedtime = datetime.datetime.now() - oldtime
		print("ImageProc - Time elapsed (s): " + str(elapsedtime.microseconds/1000000.0))
		if contours is None:
			# Clear the stream for the next frame
			updater.contoursNotFound(constants, img, oldimg)
			rawCapture.truncate(0)
			if constants.getValue("useGUI"):		
				keyupdater.update(constants, key, updater, img, oldimg)
				updater.updateGUI(constants, img, oldimg)

			if constants.getValue("senddata"):
				updater.sendData(constants.sd, 0.0, 0.0, False, False) # Tell the roboRIO that targets haven't been found yet.
			continue
		
		oldtime = datetime.datetime.now()
		pegclose = targetproc.procTarget(constants, contours, updater)
		elapsedtime = datetime.datetime.now() - oldtime
		print("TargetProc - Time elapsed (s): " + str(elapsedtime.microseconds/1000000.0))

		img = np.zeros((constants.getValue("imghpx"), constants.getValue("imgwpx"), 3), np.uint8)		
		cv2.drawContours(img, contours, -1, (0, 255, 0), cv2.FILLED)

		if pegclose:
			updater.pegclose(constants, img, oldimg)
	if constants.getValue("useGUI"):		
		keyupdater.update(constants, key, updater, img, oldimg)
		updater.updateGUI(constants, img, oldimg)
	
	# Clear the stream for the next frame
	rawCapture.truncate(0)

