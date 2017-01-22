# Import libraries
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import image # Custom library
import numpy as np

# Initialize the camera
camera = image.initCamera((640, 480))

# Let the camera warm up
time.sleep(0.1)

rawCapture = PiRGBArray(camera, size=(640, 480))

# Flags for image processing
filterHSV = False # Whether we apply HSV filtering or not

# Capture and display frames from camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):	
	
	# Get the currently pressed key
	key = cv2.waitKey(1)

	# Grab array representing image
	image = frame.array

	if key == ord("f"):
		filterHSV = not filterHSV

	if filterHSV:
		# HSV filter the image
		image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
		lower_range = np.array([80, 0, 0])
		higher_range = np.array([179, 255, 255])
		HSVmask = cv2.inRange(image, lower_range, higher_range)
		image = cv2.bitwise_and(image, image, mask=HSVmask)
		image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	# Show the frame
	cv2.imshow("Frame", image)
	
	# Clear the stream for the next frame
	rawCapture.truncate(0)

	# Break from loop if q key is pressed
	if key == ord("q"):
		break
