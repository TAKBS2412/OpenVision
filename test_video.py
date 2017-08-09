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
import numpy as np
import points
import datetime

# Create Constants
constants = Constants.Constants("settings")

# Create ImageFiltering
imagefilter = ImageFiltering.ImageFiltering()

# Create ImageProc
imageproc = ImageProc.ImageProc()

# Create TargetProc
targetproc = TargetProc.TargetProc()

# Let the camera warm up
time.sleep(0.1)

rawCapture = PiRGBArray(constants.camera, size=constants.camera.resolution)

# Prints out the HSV values for filtering
def printHSV():
	print("Upper HSV: " + str(constants.getValue("higherh")) + ", " + str(constants.getValue("highers")) + ", " + str(constants.getValue("higherv")))
	print("Lower HSV: " + str(constants.getValue("lowerh")) + ", " + str(constants.getValue("lowers")) + ", " + str(constants.getValue("lowerv")))

# Lower the shutter_speed
#constants.camera.shutter_speed = 300

# Updates all of the flags/settings based on which key was pressed.
def update(key):
	if key == ord("u"):
		constants.setValue("adjustHigher", not constants.getValue("adjustHigher"))
	if key == ord("r"):
		constants.setValue("raiseValue", constants.getValue("raiseValue") * -1)
	if key == ord("p"):
		constants.setValue("procImage", not constants.getValue("procImage"))
	elif key == ord("h"):
		if constants.getValue("adjustHigher"):
			constants.setValue("higherh", constants.getValue("higherh") + constants.getValue("raiseValue"))
			printHSV()
		else:
			constants.setValue("lowerh", constants.getValue("lowerh") + constants.getValue("raiseValue"))
			printHSV()
	elif key == ord("s"):
		if constants.getValue("adjustHigher"):
			constants.setValue("highers", constants.getValue("highers") + constants.getValue("raiseValue"))
			printHSV()
		else:
			constants.setValue("lowers", constants.getValue("lowers") + constants.getValue("raiseValue"))
			printHSV()
	elif key == ord("v"):
		if constants.getValue("adjustHigher"):
			constants.setValue("higherv", constants.getValue("higherv") + constants.getValue("raiseValue"))
			printHSV()
		else:
			constants.setValue("lowerv", constants.getValue("lowerv") + constants.getValue("raiseValue"))
			printHSV()
	if key == ord("w"):
		# Write the image files
		filename = "../Pictures/Camera Roll/" + str(datetime.datetime.now()).replace(" ", "_") # Use current date as filename.
		cv2.imwrite(filename + ".jpg", oldimg)
		cv2.imwrite(filename + "_proc.jpg", img)
		print("Images written.")
	if key == ord("i"):
		# Toggle usevideo
		constants.setValue("usevideo", not constants.getValue("usevideo"))
	if key == 81:
		constants.setValue("index", constants.getValue("index") - 1 if constants.getValue("index") > 0 else len(constants.getValue("images"))-1)
	elif key == 83:
		constants.setValue("index", constants.getValue("index") + 1 if constants.getValue("index") < len(constants.getValue("images"))-1 else 0)
	if key == ord("q"):
		constants.setValue("endloop", True)

# Capture and display frames from camera
for frame in constants.camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):	
	# Break from loop if needed.
	if constants.getValue("endloop"):
		break

	# Get the currently pressed key
	key = cv2.waitKey(1)

	# Grab array representing image
	if constants.getValue("usevideo"):
		img = frame.array
	else:
		img = cv2.imread(constants.getValue("images")[constants.getValue("index")])

	oldimg = img

	img = imagefilter.filterImage(img, constants)

	
	if constants.getValue("procImage"):
		contours = imageproc.procImage(img, constants)
		if contours is None:
			# Clear the stream for the next frame
			print("Contours not found!")
			rawCapture.truncate(0)
			update(key)
			continue

		targetproc.procTarget(constants, contours)
		
	update(key)	
	# Show the original and processed frames
	oldimgname = constants.getValue("images")[constants.getValue("index")]
	if constants.getValue("usevideo"):
		oldimgname = "Live camera feed"
	cv2.imshow(oldimgname, oldimg)
	cv2.imshow("Processed Frame", img)

	if constants.getValue("lastoldimgname") and constants.getValue("lastoldimgname") != oldimgname:
		cv2.destroyWindow(constants.getValue("lastoldimgname"))
	constants.setValue("lastoldimgname", oldimgname)
	
	# Clear the stream for the next frame
	rawCapture.truncate(0)

