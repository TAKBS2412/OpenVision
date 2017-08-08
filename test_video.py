# Import libraries
from __future__ import division
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import image # Custom library
import image_proc # Another custom library
import Constants # Yet another custom library
import numpy as np
import points
import datetime

# Create Constants
constants = Constants.Constants("settings")

# Let the camera warm up
time.sleep(0.1)

rawCapture = PiRGBArray(constants.camera, size=constants.camera.resolution)

# Prints out the HSV values for filtering
def printHSV():
	print("Upper HSV: " + str(constants.getValue("higherh")) + ", " + str(constants.getValue("highers")) + ", " + str(constants.getValue("higherv")))
	print("Lower HSV: " + str(constants.getValue("lowerh")) + ", " + str(constants.getValue("lowers")) + ", " + str(constants.getValue("lowerv")))

# Lower the shutter_speed
#constants.camera.shutter_speed = 300

# Updates all of the flags/settings based on which key was pressed.
def update(key):
	if key == ord("u"):
		constants.setValue("adjustHigher", not constants.getValue("adjustHigher"))
	if key == ord("r"):
		constants.setValue("raiseValue", constants.getValue("raiseValue") * -1)
	if key == ord("p"):
		constants.setValue("procImage", not constants.getValue("procImage"))
	elif key == ord("h"):
		if constants.getValue("adjustHigher"):
			constants.setValue("higherh", constants.getValue("higherh") + constants.getValue("raiseValue"))
			printHSV()
		else:
			constants.setValue("lowerh", constants.getValue("lowerh") + constants.getValue("raiseValue"))
			printHSV()
	elif key == ord("s"):
		if constants.getValue("adjustHigher"):
			constants.setValue("highers", constants.getValue("highers") + constants.getValue("raiseValue"))
			printHSV()
		else:
			constants.setValue("lowers", constants.getValue("lowers") + constants.getValue("raiseValue"))
			printHSV()
	elif key == ord("v"):
		if constants.getValue("adjustHigher"):
			constants.setValue("higherv", constants.getValue("higherv") + constants.getValue("raiseValue"))
			printHSV()
		else:
			constants.setValue("lowerv", constants.getValue("lowerv") + constants.getValue("raiseValue"))
			printHSV()
	if key == ord("w"):
		# Write the image files
		filename = "../Pictures/Camera Roll/" + str(datetime.datetime.now()).replace(" ", "_") # Use current date as filename.
		cv2.imwrite(filename + ".jpg", oldimg)
		cv2.imwrite(filename + "_proc.jpg", img)
		print("Images written.")
	if key == ord("i"):
		# Toggle usevideo
		constants.setValue("usevideo", not constants.getValue("usevideo"))
	if key == 81:
		constants.setValue("index", constants.getValue("index") - 1 if constants.getValue("index") > 0 else len(constants.getValue("images"))-1)
	elif key == 83:
		constants.setValue("index", constants.getValue("index") + 1 if constants.getValue("index") < len(constants.getValue("images"))-1 else 0)
	if key == ord("q"):
		constants.setValue("endloop", True)

# Capture and display frames from camera
for frame in constants.camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):	
	# Break from loop if needed.
	if constants.getValue("endloop"):
		break

	# Get the currently pressed key
	key = cv2.waitKey(1)

	# Grab array representing image
	if constants.getValue("usevideo"):
		img = frame.array
	else:
		img = cv2.imread(constants.getValue("images")[constants.getValue("index")])

	# Blur the image
	img = cv2.GaussianBlur(img, (5, 5), 0)
	
	oldimg = img

	# HSV filter the image
	img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	lower_range = np.array([constants.getValue("lowerh"), constants.getValue("lowers"), constants.getValue("lowerv")])
	higher_range = np.array([constants.getValue("higherh"), constants.getValue("highers"), constants.getValue("higherv")])
	HSVmask = cv2.inRange(img, lower_range, higher_range)
	img = cv2.bitwise_and(img, img, mask=HSVmask)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	# Process the image
	if constants.getValue("procImage"):
		contours = image.getSecondLargestContour(img)
		if contours is None:
			# Clear the stream for the next frame
			rawCapture.truncate(0)
			print("Contours not found!")
			update(key)
			continue
		largestCnt, secondLargestCnt = contours
		if largestCnt is None or secondLargestCnt is None:
			# Clear the stream for the next frame
			print("Contours not found!")
			rawCapture.truncate(0)
			update(key)
			continue

		_x, _y, wpx, hpx = cv2.boundingRect(largestCnt)
		print("Ratio: " + str(hpx/wpx))
		
				
		# Find the centroid's coordinates
		cntcoords = image.getContourCentroidCoords(largestCnt)
		cnt2coords = image.getContourCentroidCoords(secondLargestCnt)
		if cntcoords == None or cnt2coords == None:
			pass
		else:
			cx, cy = cntcoords
			cx2, cy2 = cnt2coords
			pegx = (cx + cx2) / 2 # Find the x-coord of the peg (the average of the x-coordinates of the two vision targets)
			
			# Print out information
			print("Centroid coordinates: (" + str(cx) + ", " + str(cy) + ")")
			print("Height (px): " + str(hpx))
			print("Width (px): " + str(wpx))
			distance = image_proc.getDistance(constants.imghpx, 5.08, hpx, constants.getValue("viewangle"))
			print("Distance (cm): " + str(distance))
			print("Angle (radians): " + str(image_proc.getHorizAngle(constants.imgwpx, 5.08, distance, hpx, pegx)))


	update(key)	
	# Show the original and processed frames
	oldimgname = constants.getValue("images")[constants.getValue("index")]
	if constants.getValue("usevideo"):
		oldimgname = "Live camera feed"
	cv2.imshow(oldimgname, oldimg)
	cv2.imshow("Processed Frame", img)

	if constants.getValue("lastoldimgname") and constants.getValue("lastoldimgname") != oldimgname:
		cv2.destroyWindow(constants.getValue("lastoldimgname"))
	constants.setValue("lastoldimgname", oldimgname)
	
	# Clear the stream for the next frame
	rawCapture.truncate(0)

