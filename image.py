# Import libraries
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import image_proc
import numpy as np
import sys

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
# res - the resolution of the image, as a tuple (width, height)
# lowerh, lowers, lowerv - lower HSV values for filtering
# higherh, highers, higherv - higher HSV values for filtering
def procImage(image, res, lowerh, lowers, lowerv, higherh, highers, higherv):
	
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
		print(str(percentFilled) + "%")

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
	# Sort the contours using DSU (Decorate-Sort-Undecorate)
	# "Decorate" the array
	decorated = [(cv2.contourArea(cnt), cv2.contourArea(cnt)/cv2.contourArea(np.int0(cv2.boxPoints(cv2.minAreaRect(cnt)))) if cv2.contourArea(np.int0(cv2.boxPoints(cv2.minAreaRect(cnt)))) else 0, cnt) for cnt in contours]
	npDecorated = np.array(decorated, dtype=object)
	# Sort the array
	sortedarr = np.sort(npDecorated)	

# Finds the largest and second-largest contour in the processed image
# image - the HSV-filtered image to process
# Returns None if no targets were found
# Otherwise, returns an array - the first element is the largest contour, the second is the second-largest contour
def getSecondLargestContour(image):
	# Find contours
	image, contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)

	# If no contours have been found, quit
	if len(contours) == 0:
		#sys.exit("Error: No targets found!")
		return None

	# Find the largest contour
	largestCntArea = 0 # Area of the largest contour
	largestCnt = None
	secondLargestCntArea = 0 # Area of the second largest contour
	secondLargestCnt = None
	for cnt in contours:
		cntArea = cv2.contourArea(cnt)
		a = cv2.minAreaRect(cnt)
		b = cv2.boxPoints(a)
		c = np.int0(b)
		polygonArea = cv2.contourArea(c)
		if polygonArea == 0: continue
		percentFilled = cntArea/polygonArea*100
		if percentFilled < 80: continue
		print(str(percentFilled) + "%")

		if cntArea > largestCntArea:
			secondLargestCntArea = largestCntArea
			secondLargestCnt = largestCnt
			largestCntArea = cntArea
			largestCnt = cnt
		elif cntArea > secondLargestCntArea:
			secondLargestCntArea = cntArea
			secondLargestCnt = cnt
	return [largestCnt, secondLargestCnt]



# Finds the x and y coordinates of the contours's centroid
# Returns an array with the centroid's x and y coordinates as the first and second elements
def getContourCentroidCoords(contour):
	M = cv2.moments(contour)
	cx = int(M["m10"]/M["m00"])
	cy = int(M["m01"]/M["m00"])
	return [cx, cy]



