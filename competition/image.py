# Import libraries
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import image_proc
import numpy as np
import sys
import TargetProc

# Initializes the camera
def initCamera(res):
	# Initialize the camera
	camera = PiCamera()
	camera.resolution = res
	
	# Allow the camera to sleep
	time.sleep(0.1)
	
	return camera

# Takes a picture from the camera
def takePicture(camera):
	# Grab an image
	capture = PiRGBArray(camera)
	camera.capture(capture, format="bgr")

	return capture.array

# Process the image (apply HSV filtering, convert to greyscale)
# image - the image to process
# lowerh, lowers, lowerv - lower HSV values for filtering
# higherh, highers, higherv - higher HSV values for filtering
def procImage(image, lowerh, lowers, lowerv, higherh, highers, higherv):
	
	# Blur the image
	image = cv2.GaussianBlur(image, (5, 5), 0)

	# Convert image to HSV
	image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

	# Create HSV color range
	lower_range = np.array([lowerh, lowers, lowerv])
	higher_range = np.array([higherh, highers, higherv])

	# Filter out image according to HSV color range
	HSVmask = cv2.inRange(image, lower_range, higher_range)
	image = cv2.bitwise_and(image, image, mask=HSVmask)

	# Convert to greyscale
	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	return image

# Returns an array with the centroid's x and y coordinates as the first and second elements
def getContourCentroidCoords(contour):
	M = cv2.moments(contour)
	if M["m00"] == 0:
		return None
	cx = int(M["m10"]/M["m00"])
	cy = int(M["m01"]/M["m00"])
	return [cx, cy]

