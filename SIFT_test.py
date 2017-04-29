from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import cv2
import image
import time

targetimg = cv2.imread("cropped.jpg", 0)

# Initiate SIFT detector
sift = cv2.xfeatures2d.SIFT_create()

# Find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(targetimg,None)

# Initialize the camera
camera = image.initCamera((640, 480))

# Let the camera warm up
time.sleep(0.1)

rawCapture = PiRGBArray(camera, size=(640, 480))

# Lower the shutter_speed
camera.shutter_speed = 100

# Capture and display frames from camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):	
	img = frame.array
	kp2, des2 = sift.detectAndCompute(img,None)
	print("Hello")
	rawCapture.truncate(0)

