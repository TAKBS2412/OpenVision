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

# Flags for image processing

procImage = False # Whether to calculate distance or not

# HSV Values to filter
lowerh = 50
lowers = 200
lowerv = 30 #8 for red raspberry pi

higherh = 65
highers = 255
higherv = 255 # 45 for red raspberry pi

adjustHigher = True # Whether to adjust the higher or lower HSV values
raiseValue = 1 # If raiseValue is 1, then 1 will be added to the HSV values; if raiseValue is -1, then 1 will be subtracted from the HSV values

usevideo = True # Whether to read from video or from a file

endloop = False

index = 0 # Array index for which image to process (in the above array, images)

lastoldimgname = ""

# Prints out the HSV values for filtering
def printHSV():
	print("Upper HSV: " + str(higherh) + ", " + str(highers) + ", " + str(higherv))
	print("Lower HSV: " + str(lowerh) + ", " + str(lowers) + ", " + str(lowerv))

# Lower the shutter_speed
#constants.camera.shutter_speed = 300

# Updates all of the flags/settings based on which key was pressed.
def update(key):
	global adjustHigher, raiseValue, procImage, higherh, highers, higherv, lowerh, lowers, lowerv, usevideo, index, endloop
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
		filename = "../Pictures/Camera Roll/" + str(datetime.datetime.now()).replace(" ", "_") # Use current date as filename.
		cv2.imwrite(filename + ".jpg", oldimg)
		cv2.imwrite(filename + "_proc.jpg", img)
		print("Images written.")
	if key == ord("i"):
		# Toggle usevideo
		usevideo = not usevideo
	if key == 81:
		index = index - 1 if index > 0 else len(constants.images)-1
	elif key == 83:
		print("test")
		index = index + 1 if index < len(constants.images)-1 else 0
	if key == ord("q"):
		endloop = True

# Capture and display frames from camera
for frame in constants.camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):	
	# Break from loop if needed.
	if endloop:
		break

	# Get the currently pressed key
	key = cv2.waitKey(1)

	# Grab array representing image
	if usevideo:
		img = frame.array
	else:
		img = cv2.imread(constants.images[index])

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
		
		epsilon = 0.05*cv2.arcLength(largestCnt, True)
		approx = cv2.approxPolyDP(largestCnt, epsilon, True)
		pts = []
		for point in approx:
			pts.append(point[0])
		pts = np.array(pts)
		
		boundingrect = cv2.minAreaRect(largestCnt)
		print("Boundingrect: " + str(boundingrect))
		pts = points.find_points(boundingrect)
		straight_pts = np.insert(points.find_straight_rect(pts), 2, 0, axis = 1)
		
		# Find rotation vector from pts and straight_pts
		#s = np.array([[1288.28889, 0, 74.5903466], [0, 1291.14257, 153.495243], [0, 0, 1]])
		s = np.array([[1, 0, 1], [0, 1, 1], [0, 0, 1]])
		retval, rvec, tvec = cv2.solvePnP(straight_pts, pts, s, None)
		print(rvec)

	
		'''
		
		pts = points.order_points(pts)
	
		# Find the horizontal skew from pts and using the distance formula.
		left_height = np.abs(np.sqrt((pts[0][0] - pts[3][0])**2 + (pts[0][1] - pts[3][1])**2))
		print("Left height: " + str(left_height))

		right_height = np.abs(np.sqrt((pts[2][0] - pts[1][0])**2 + (pts[2][1] - pts[1][1])**2))
		print("Right height: " + str(right_height))

		left_distance = image_proc.getDistance(constants.imghpx, 5.08, left_height, constants.viewangle)
		print("Left distance: " + str(left_distance))

		right_distance = image_proc.getDistance(constants.imghpx, 5.08, right_height, constants.viewangle)
		print("Right distance: " + str(right_distance))

		delta_distance = right_distance - left_distance
		print("Delta distance: " + str(delta_distance))
		
		print(delta_distance)
		skew = np.arcsin(delta_distance/5.08)
		print("Calculated skew: " + str(skew))


		left_width = np.abs(np.sqrt((pts[0][0] - pts[1][0])**2 + (pts[0][1] - pts[1][1])**2))
		right_width = np.abs(np.sqrt((pts[2][0] - pts[3][0])**2 + (pts[2][1] - pts[3][1])**2))

		wpx = max(left_width, right_width)
		hpx = max(left_height, right_height)

		wpx = min(boundingrect[1])
		hpx = max(boundingrect[1])
		'''

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
			distance = image_proc.getDistance(constants.imghpx, 5.08, hpx, constants.viewangle)
			print("Distance (cm): " + str(distance))
			print("Angle (radians): " + str(image_proc.getHorizAngle(constants.imgwpx, 5.08, distance, hpx, pegx)))


	update(key)	
	# Show the original and processed frames
	oldimgname = constants.images[index]
	if usevideo:
		oldimgname = "Live camera feed"
	cv2.imshow(oldimgname, oldimg)
	cv2.imshow("Processed Frame", img)

	if lastoldimgname and lastoldimgname != oldimgname:
		cv2.destroyWindow(lastoldimgname)
	lastoldimgname = oldimgname
	
	# Clear the stream for the next frame
	rawCapture.truncate(0)

