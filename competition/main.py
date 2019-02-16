# Import libraries
from __future__ import division
from picamera.array import PiRGBArray
from picamera import PiCamera
import os
import sys
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
import Networking
import FPS
import numpy as np
import PiVideoStream
import printer
#import points

# Read command-line arguments
defaultsettingspath = "/home/pi/src/competition/settings"
currentsettingspath = defaultsettingspath
if len(sys.argv) == 2:
	currentsettingspath = sys.argv[1]

# Create Constants
constants = Constants.Constants(currentsettingspath)

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

# Create Networking
networking = Networking.Networking(constants)

# Threaded video stream
vs = PiVideoStream.PiVideoStream(constants, resolution=(constants.getValue("imgwpx"), constants.getValue("imghpx"))).start()

# Lower the shutter_speed
vs.camera.shutter_speed = constants.getValue("shutterspeed")

# Let the camera warm up
time.sleep(2.0)

# FPS tracker
fps = FPS.FPS()

# The contours from Imageproc
contours = None

# If we're checked the image paths to see if they're directories or not
dirschecked = False

# Capture and display frames from camera
try:
	while True:
		# Break from loop if needed.
		if constants.getValue("endloop"):
			vs.stop()
			break
		
		# Get the currently pressed key if useGUI is enabled.
		if constants.getValue("useGUI"):
			key = cv2.waitKey(1)

		# Grab array representing image
		if constants.getValue("usevideo"):
			oldimg, img = vs.read()
		else:
			allimgs = constants.getValue("images")
			if not dirschecked:
				for index, imgpath in enumerate(allimgs):
					if os.path.isdir(imgpath):
						innerfiles = []
						# Use this instead of a list comprehension so we don't compute joinedname more than once
						for filename in os.listdir(imgpath):
							joinedname = os.path.join(imgpath, filename)
							if os.path.isfile(joinedname):
								innerfiles.append(joinedname)

						allimgspart1 = allimgs[:index]
						allimgspart2 = allimgs[index+1:]
						allimgs = allimgspart1 + innerfiles + allimgspart2
						constants.setValue("images", allimgs)
				dirschecked = True

			oldimg = img = cv2.imread(constants.getValue("images")[constants.getValue("index")])
			img = imagefilter.filterImage(img, constants)
		if img is None:
			vs.stop()
			break

		if constants.getValue("procImage"):
			contours = imageproc.procImage(img, constants)
			if contours is None or len(contours) == 0:
				updater.contoursNotFound(constants, img, oldimg)
			
				if constants.getValue("senddata"):
					networking.sendData(constants, 0.0, 0.0, False, False) # Tell the roboRIO that targets haven't been found yet.
			else:
				doextake = targetproc.procTarget(constants, contours, updater, networking, imageproc.approx, img)
				if doextake:
					updater.doextake(constants, img, oldimg)

		if constants.getValue("useGUI"):
			if contours is not None:
				img = np.zeros((constants.getValue("imghpx"), constants.getValue("imgwpx"), 3), np.uint8)		
				cv2.drawContours(img, contours, -1, (0, 255, 0), cv2.FILLED)
			keyupdater.update(constants, key, updater, img, oldimg)
			updater.updateGUI(constants, img, oldimg)
		
		fps.update(constants)
except KeyboardInterrupt:
	if constants.getValue("printdata"):
		printer.printIfNeeded("Interrupted! Exiting...", constants)

cv2.destroyAllWindows()	
vs.stop()
