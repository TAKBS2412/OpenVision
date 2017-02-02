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

# HSV Values to filter
lowerh = 60
lowers = 0
lowerv = 0#255

higherh = 90#91
highers = 255#163
higherv = 255

adjustHigher = True # Whether to adjust the higher or lower HSV values
raiseValue = 1 # If raiseValue is 1, then 1 will be added to the HSV values; if raiseValue is -1, then 1 will be subtracted from the HSV values
# Image resolution
resolution = camera.resolution
imgwpx, imghpx = resolution

# Prints out the HSV values for filtering
def printHSV():
	print("Upper HSV: " + str(higherh) + ", " + str(highers) + ", " + str(higherv))
	print("Lower HSV: " + str(lowerh) + ", " + str(lowers) + ", " + str(lowerv))

# Capture and display frames from camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):	
	
	# Get the currently pressed key
	key = cv2.waitKey(1)

	# Grab array representing image
	img = frame.array
	oldimg = img

	if key == ord("u"):
		adjustHigher = not adjustHigher

	if key == ord("r"):
		raiseValue *= -1
	
	# HSV filter the image
	img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	lower_range = np.array([lowerh, lowers, lowerv])
	higher_range = np.array([higherh, highers, higherv])
	HSVmask = cv2.inRange(img, lower_range, higher_range)
	img = cv2.bitwise_and(img, img, mask=HSVmask)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	if key == ord("p"):
		# Process the image
		largestCnt = image.getLargestContour(img)
		boundingrect = cv2.minAreaRect(largestCnt)
		wpx, hpx = boundingrect[1]
		viewangle = 0.698

		print("Height (px): " + str(hpx))
		print("Width (px): " + str(wpx))
		distance = image_proc.getDistance(imghpx, 5.08, hpx, viewangle)
		print("Distance (cm): " + str(distance))
		print("Angle (radians): " + str(image_proc.getHorizAngle(imghpx, 5.08, distance, hpx, image.getContourCentroidCoords(largestCnt)[0])))
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


