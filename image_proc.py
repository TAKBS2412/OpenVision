# Import libraries
from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np
import time

# Finds the camera view angle
# This function takes the following parameters:
# hpx - height of the image in pixels
# tcm - height of the target in cm
# d - distance in cm
# tpx - height of the target in px
def getViewAngle(hpx, tcm, d, tpx):
	return 2 * np.arctan((hpx*tcm)/(2*d*tpx))

# Finds the distance to the target
# This function takes the following parameters:
# hpx - height of the image in pixels
# tcm - height of the target in cm
# tpx - height of the target in px
# theta - view angle of the camera
def getDistance(hpx, tcm, tpx, theta):
	return (hpx*tcm)/(2*tpx*np.tan(theta/2))

# Finds the angle from the target to the middle of the robot's field of view
# The contour is an array of array representing the target, and it's centroid is located roughly in the center
# This function takes the following parameters:
# hpx - height of the image in pixels
# tcm - height of the target in cm
# d - distance in cm
# tpx - height of the target in px
# cx - x-coord. of the contour's centroid
def getHorizAngle(hpx, tcm, d, tpx, cx):
	return np.arctan((tcm*(cx/2-hpx))/(d*tpx))
