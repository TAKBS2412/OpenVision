# Import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import numpy as np
import image_proc
import sys

# Starts the camera
def initCamera(camera):
	# Grab a reference to the raw camera capture
	rawCapture = PiRGBArray(camera)

	# Give some time for the camera to warm up
	time.sleep(0.1)
	
	return rawCapture

# Simple utility function for taking a picture from the camera
def getImage(camera, rawCapture, format="bgr"):
	# Grab an image
	camera.capture(rawCapture, format=format)
	image = rawCapture.array
	
	return image

# Initialize the camera
camera = PiCamera()

# Alter the camera resolution
imgwidthpx = 640
imgheightpx = 480
camera.resolution = (imgwidthpx, imgheightpx)

#imgwidthpx, imgheightpx = camera.resolution
# Startup the camera
rawCapture = initCamera(camera)

# Take a picture 
image = getImage(camera, rawCapture)
oldimage = image

# Save the image
cv2.imwrite("oldimage.jpg", oldimage)

# Display the unprocessed image
cv2.imshow("OldImage", image)

# IMAGE PROCESSING GOES HERE

oldtime = time.time()

# Convert to HSV
image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Define HSV color range
lower_color = np.array([90, 50, 50])
upper_color = np.array([130, 255, 255])

# Filter out all other colors that aren't in the HSV color range
mask = cv2.inRange(image, lower_color, upper_color)

# Bitwise AND mask and original image
image = cv2.bitwise_and(oldimage, oldimage, mask=mask)

# Convert to greyscale
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

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
targetheightcm = 10
print("Target Height (cm): " + str(targetheightcm))
boundingrect = cv2.minAreaRect(largestCnt)
targetwidthpx, targetheightpx = boundingrect[1]
print("Image Height (px): " + str(imgheightpx))
print("Target Height (px): " + str(targetwidthpx))
viewangle = 0.698/2.0
print("Viewangle (Radians) : " + str(viewangle))

# Calculate distance
targetdistancecm = image_proc.getdistance(targetheightcm, imgheightpx, targetheightpx, viewangle, output=True)

# Calculate target's horizontal angle based on centroid's location compared to middle of image
image_proc.gethorizangle(cx, imgwidthpx, targetheightcm, targetdistancecm, targetheightpx, output=True)

print "Time spent: ",
print "%.20f" % (time.time() - oldtime)


# Save the processed image
cv2.imwrite("processed.jpg", image)

# Display the processed image on screen and wait for a keypress
cv2.imshow("Image", image)
cv2.waitKey(0)
