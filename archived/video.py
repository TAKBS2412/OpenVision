# Import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import sys
import image_proc

# Initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
 
# Allow the camera to warmup
time.sleep(0.1)

# Flags for displaying the image
filterimg = False # Whether to filter and display the image

# Hue, Saturation, and Value values for HSV filtering
lowerh = 90
lowers = 50
lowerv = 50

higherh = 130
highers = 255
higherv = 250

# Find the camera resolution
imgwidthpx, imgheightpx = camera.resolution

# Capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# Grab the raw NumPy array representing the image, then initialize the timestamp
	image = frame.array
	oldimage = image

	# Get the key pressed 
	key = cv2.waitKey(1) & 0xFF

	if key == ord("f"):
		filterimg = not filterimg # Toggle the filterimg flag

	if filterimg:
		# Convert to HSV
		image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

		# Define HSV color range
		lower_color = np.array([lowerh, lowers, lowerv], dtype=np.uint8)
		upper_color = np.array([higherh, highers, higherv], dtype=np.uint8)

		# Filter out all other colors that aren't in the HSV color range
		mask = cv2.inRange(image, lower_color, upper_color)

		# Bitwise AND mask and original image
		image = cv2.bitwise_and(oldimage, oldimage, mask=mask)

		# Convert to greyscale
		image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

		# Blur the image
		image = cv2.GaussianBlur(image, (5, 5), 0)

		if key == ord("p"):
			# Actually filter and process the image
			oldtime = time.time()
			
			# Find contours
			image, contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)

			# If no contours have been found, quit
			if len(contours) == 0:
				sys.exit("Error: No targets found!")
			
			# Find the largest contour
			largestCntArea = 0 # Area of the largest contour
			largestCnt = None
			for cnt in contours:
				cntArea = cv2.contourArea(cnt)
				if cntArea > largestCntArea:
					largestCntArea = cntArea
					largestCnt = cnt
			print(len(largestCnt))

			# Find the centroid of the largest contour
			M = cv2.moments(largestCnt)
			cx = int(M["m10"]/M["m00"])
			cy = int(M["m01"]/M["m00"])
			print("(" + str(cx) + ", " + str(cy) + ")")

			# Print target and image height stats
			targetheightcm = 20
			print("Target Height (cm): " + str(targetheightcm))
			boundingrect = cv2.minAreaRect(largestCnt)
			targetwidthpx, targetheightpx = boundingrect[1]
			print("Image Height (px): " + str(imgheightpx))
			print("Target Height (px): " + str(targetheightpx))
			viewangle = 0.698/2.0
			print("Viewangle (Radians) : " + str(viewangle))


			print(boundingrect)
			# Calculate distance
			targetdistancecm = image_proc.getdistance(targetheightcm, imgheightpx, targetheightpx, viewangle, output=True)

			# Calculate target's horizontal angle based on centroid's location compared to middle of image
			image_proc.gethorizangle(cx, imgwidthpx, targetheightcm, targetdistancecm, targetheightpx, output=True)

			print "Time spent: ",
			print "%.20f" % (time.time() - oldtime)



	# Show the frame
	cv2.imshow("Frame", image)
	 
	# Clear the stream in preparation for the next frame
	rawCapture.truncate(0)
 
	# If the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
