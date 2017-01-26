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
	img = image.procImage(img, resolution, 80, 40, 0, 130, 255, 200)

	largestCnt = image.getLargestContour(img)
	boundingrect = cv2.minAreaRect(largestCnt)
	wpx, hpx = boundingrect[1]
	viewangle = 0.698

	print("Height (px): " + str(hpx))
	print("Width (px): " + str(wpx))
	distance = image_proc.getDistance(imghpx, 5.08, hpx, viewangle)
	print("Distance (cm): " + str(distance))
	print("Angle (radians): " + str(image_proc.getHorizAngle(imghpx, 5.08, distance, hpx, image.getContourCentroidCoords(largestCnt)[0])))

	cv2.imshow("Frame", img)
	cv2.waitKey(0)


main()
