# Import libraries
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import image # Custom library
import image_proc # Another custom library
import numpy as np

# Initialize the camera
camera = image.initCamera((640, 480))

# Let the camera warm up
time.sleep(0.1)

rawCapture = PiRGBArray(camera, size=(640, 480))

# Flags for image processing

procImage = False # Whether to calculate distance or not

# HSV Values to filter
lowerh = 50
lowers = 235
lowerv = 30 #8 for red raspberry pi

higherh = 65
highers = 255
higherv = 80 # 45 for red raspberry pi

adjustHigher = True # Whether to adjust the higher or lower HSV values
raiseValue = 1 # If raiseValue is 1, then 1 will be added to the HSV values; if raiseValue is -1, then 1 will be subtracted from the HSV values
# Image resolution
resolution = camera.resolution
imgwpx, imghpx = resolution

# Prints out the HSV values for filtering
def printHSV():
	print("Upper HSV: " + str(higherh) + ", " + str(highers) + ", " + str(higherv))
	print("Lower HSV: " + str(lowerh) + ", " + str(lowers) + ", " + str(lowerv))

# Lower the shutter_speed
camera.shutter_speed = 200

# Capture and display frames from camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):	
	
	# Get the currently pressed key
	key = cv2.waitKey(1)

	# Grab array representing image
	img = frame.array

	# Blur the image
	img = cv2.GaussianBlur(img, (5, 5), 0)
	
	oldimg = img

	# HSV filter the image
	img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	lower_range = np.array([lowerh, lowers, lowerv])
	higher_range = np.array([higherh, highers, higherv])
	HSVmask = cv2.inRange(img, lower_range, higher_range)
	img = cv2.bitwise_and(img, img, mask=HSVmask)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	# Process the image
	if procImage:
		largestCnt, secondLargestCnt = image.getSecondLargestContour(img)
		boundingrect = cv2.minAreaRect(largestCnt)
		wpx = max(boundingrect[1])
		hpx = min(boundingrect[1])
		print(len(boundingrect[1]))	
		
		viewangle = 0.726
		
		# Find the centroid's coordinates
		cx, cy = image.getContourCentroidCoords(largestCnt)
		cx2, cy2 = image.getContourCentroidCoords(secondLargestCnt)
		pegx = (cx + cx2) / 2 # Find the x-coord of the peg (the average of the x-coordinates of the two vision targets)

		# Print out information
		print("Centroid coordinates: (" + str(cx) + ", " + str(cy) + ")")
		print("Height (px): " + str(hpx))
		print("Width (px): " + str(wpx))
		distance = image_proc.getDistance(imghpx, 5.08, hpx, viewangle)
		print("Distance (cm): " + str(distance))
		print("Angle (radians): " + str(image_proc.getHorizAngle(imgwpx, 5.08, distance, hpx, pegx)))


	if key == ord("u"):
		adjustHigher = not adjustHigher
	if key == ord("r"):
		raiseValue *= -1
	if key == ord("p"):
		procImage = not procImage
	elif key == ord("h"):
		if adjustHigher:
			higherh += raiseValue
			printHSV()
		else:
			lowerh += raiseValue
			printHSV()
	elif key == ord("s"):
		if adjustHigher:
			highers += raiseValue
			printHSV()
		else:
			lowers += raiseValue
			printHSV()
	elif key == ord("v"):
		if adjustHigher:
			higherv += raiseValue
			printHSV()
		else:
			lowerv += raiseValue
			printHSV()
	if key == ord("w"):
		# Write the image files
		cv2.imwrite("orig.jpg", oldimg)
		cv2.imwrite("proc.jpg", img)
		print("Images written.")

	# Show the original and processed frames
	cv2.imshow("Original Frame", oldimg)
	cv2.imshow("Processed Frame", img)
	
	# Clear the stream for the next frame
	rawCapture.truncate(0)

	# Break from loop if q key is pressed
	if key == ord("q"):
		break


