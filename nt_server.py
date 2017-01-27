import sys
import time
from networktables import NetworkTables

import logging
logging.basicConfig(level=logging.DEBUG)

import image
import image_proc

ip = "roborio-2412-frc.local"

NetworkTables.initialize(server=ip)

sd = NetworkTables.initialize(server=ip)

imgwpx = 640
imghpx = 480
resolution = (imgwpx, imghpx) 
camera = image.initCamera(resolution)


while True:
	# Do vision processing stuff here
	angle = distance = 0 # Default values
	targetsFound = False
	# The vision processing stuff below will set the above variables
	img = image.takePicture(camera)
	img = image.procImage(img, resolution, 80, 40, 0, 130, 255, 200)
	largestCnt = image.getLargestContour(img)
	if largestCnt == None:
		# No targets found
		targetsFound = False
	else:
		boundingrect = cv2.minAreaRect(largestCnt)
		wpx, hpx = boundingrect[1]
		viewangle = 0.698
		distance = image_proc.getDistance(imghpx, 5.08, hpx, viewangle)
		angle = image_proc.getHorizAngle(imghpx, 5.08, distance, hpx, image.getContourCentroidCoords(largestCnt)[0])
	
	# Send the variables to the roboRIO
	sd.putNumber("angle", angle)
	sd.putNumber("distance", distance)
	sd.putBoolean("targetsFound", targetsFound)