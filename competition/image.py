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

# Finds the largest contour in the processed image
# image - the HSV-filtered image to process
# Returns None if no targets were found
def getLargestContour(image):
	# Find contours
	image, contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)

	# If no contours have been found, quit
	if len(contours) == 0:
		#sys.exit("Error: No targets found!")
		return None

	# Find the largest contour
	largestCntArea = 0 # Area of the largest contour
	largestCnt = None
	for cnt in contours:
		cntArea = cv2.contourArea(cnt)
		a = cv2.minAreaRect(cnt)
		b = cv2.boxPoints(a)
		polygonArea = cv2.contourArea(b)
		if polygonArea == 0: continue
		percentFilled = cntArea/polygonArea*100
		if percentFilled < 80: continue

		if cntArea > largestCntArea:
			largestCntArea = cntArea
			largestCnt = cnt
	return largestCnt

# Finds all the contours in the image iamge and sorts them by size (largest to smallest)
# Returns an array of the sorted contours. If no contours have been found, returns an empty array
def sortContours(image):
	# Find contours
	image, contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)

	# If no contours have been found, quit
	if len(contours) == 0:
		#sys.exit("Error: No targets found!")
		return []
	
	return sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

# Checks the contour to make sure it fulfills the requirements (nonzero size, rectangular, etc.)
# TODO: Make this function accept array of functions (for checking the contour) as a parameter
def checkContour(cnt):
	cntArea = cv2.contourArea(cnt)
	approx = cv2.approxPolyDP(cnt, 0.05*cv2.arcLength(cnt, True), True)
	if len(approx) != 4: return False # Make sure the contour's rectangular

	polygonArea = cv2.contourArea(approx)
	if polygonArea == 0 or cntArea == 0: return False # Make sure the contour has a nonzero area
	percentFilled = polygonArea/cntArea*100
	if percentFilled < 70: return False # Make sure the contour is filled

	return True


# Finds the largest and second-largest contour in the processed image
# image - the HSV-filtered image to process
# Returns None if no targets were found
# Otherwise, returns an array - the first element is the largest contour, the second is the second-largest contour
def getSecondLargestContour(image):
	# Find contours
	#image, contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)

	# Find sorted list of contours
	contours = sortContours(image)
	
	# If no contours have been found, quit
	if len(contours) == 0:
		#sys.exit("Error: No targets found!")
		return None

	# Filter the list based on checkContour()
	filteredcontours = [cnt for cnt in contours if checkContour(cnt)]

	return filteredcontours[:2]

# Finds the x and y coordinates of the contours's centroid
# Returns an array with the centroid's x and y coordinates as the first and second elements
def getContourCentroidCoords(contour):
	M = cv2.moments(contour)
	if M["m00"] == 0:
		return None
	cx = int(M["m10"]/M["m00"])
	cy = int(M["m01"]/M["m00"])
	return [cx, cy]



