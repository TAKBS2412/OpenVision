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
filterHSV = False # Whether we apply HSV filtering or not

# Image resolution
resolution = camera.resolution
imgwpx, imghpx = resolution

# Capture and display frames from camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):	
	
	# Get the currently pressed key
	key = cv2.waitKey(1)

	# Grab array representing image
	img = frame.array

	if key == ord("f"):
		filterHSV = not filterHSV
	
	if filterHSV:
		# HSV filter the image
		img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
		lower_range = np.array([80, 40, 0])
		higher_range = np.array([130, 255, 200])
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

	# Show the frame
	cv2.imshow("Frame", img)
	
	# Clear the stream for the next frame
	rawCapture.truncate(0)

	# Break from loop if q key is pressed
	if key == ord("q"):
		break
