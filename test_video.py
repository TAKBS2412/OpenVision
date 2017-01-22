# Import libraries
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import image # Custom library

# Initialize the camera
camera = image.initCamera((640, 480))

# Let the camera warm up
time.sleep(0.1)

rawCapture = PiRGBArray(camera, size=(640, 480))

# Capture and display frames from camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):	

	# Grab array representing image
	image = frame.array
		
	# Show the frame
	cv2.imshow("Frame", image)
	
	# Get the currently pressed key
	key = cv2.waitKey(1)

	# Clear the stream for the next frame
	rawCapture.truncate(0)

	# Break from loop if q key is pressed
	print(chr(key))
	if key == ord("q"):
		break
