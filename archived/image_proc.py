# Python script for Image processing
# Import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np

# NOTES:
# All measurements of distance are in cm unless otherwise specified
# All angles are in radians unless otherwise specified

# Finds the camera view angle, given the distance, image height (px), and target height (px AND cm)
# If output is set to true, prints output
# Returns an array of angles - the first element is the camera's view angle in radians, the second element is the angle in degrees
def getviewangle(imgheightpx, targetheightcm, targetdistancecm, targetheightpx, output=False):
	if output:
		print("Target Distance (cm): " + str(targetdistancecm))
	# Calculate view angle (in radians)
	viewangle = 2*np.arctan((imgheightpx * targetheightcm) / (2 * targetdistancecm * targetheightpx))
	if output:
		print("Viewangle (Radians) : " + str(viewangle))
		print("Viewangle (Degrees) : " + str(viewangle * 360 / (2 * np.pi)))
	return viewangle

# Finds the distance, given the target height (px AND cm), viewangle, and image height (px)
# If output is set to true, prints output
# Returns the distance
def getdistance(targetheightcm, imgheightpx, targetheightpx, viewangle, output=False):
	targetdistancecm = (targetheightcm * imgheightpx)/(2 * targetheightpx * np.tan(viewangle))
	if output:
		print("Target Distance (cm) : " + str(targetdistancecm))
	return targetdistancecm

# Finds the target's horizontal angle, given the centroid's x-coordinate, image width (px), target height (px AND cm), and target distance
def gethorizangle(cx, imgwidthpx, targetheightcm, targetdistancecm, targetheightpx, output=False):
	deltax = cx - (imgwidthpx/2.0) # Difference between centroid location and middle of image (x-axis)
	horizangle = np.arctan((deltax * targetheightcm) / (targetdistancecm * targetheightpx))
	if output:
		print("Horizontal Angle (Radians) : " + str(horizangle))
		print("Horizontal Angle (Degrees) : " + str(horizangle * 360 / (2 * np.pi)))
	return horizangle

