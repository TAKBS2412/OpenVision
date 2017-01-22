# Import libraries
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import image_proc
import image
import numpy as np

def main():
	imgwpx = 640
	imghpx = 480
	resolution = (imgwpx, imghpx) 
	camera = image.initCamera(resolution)
	img = image.takePicture(camera)
	img = image.procImage(img, resolution, 90, 50, 50, 130, 255, 255)
	cv2.imshow("Frame", img)
	cv2.waitKey()
	largestCnt = image.getLargestContour(img)
	print(largestCnt)
	boundingrect = cv2.minAreaRect(largestCnt)
	wpx, hpx = boundingrect[1]
	viewangle = 0.698/2.0
	print("Distance (cm): " + str(image_proc.getDistance(imghpx, 20, hpx, viewangle)))
main()
