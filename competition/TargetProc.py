import cv2
import numpy as np
import image # Custom library
import image_proc # Another custom library
import printer # Library for printing

INCHES_TO_CM = 2.54
TARGET_HEIGHT_CM = 5.5 * INCHES_TO_CM

'''
A class that processes targets.
'''
class TargetProc:
	# Calculates the distance, angle, and height to width ratio of the specified contour.
	def procTarget(self, constants, contours, updater, networking, img):
		largestCnt = contours[0]

		onecnt = False
		left = True
		offx = 8 / 2 * 2.54 # Halve the 8 inches and convert to cm

		imghpx = constants.getValue("imghpx")
		imgwpx = constants.getValue("imgwpx")

		# Make the center of the contours default to the middle of the image
		cx = imgwpx / 2.0
		cy = imghpx / 2.0

		# Find the top two and bottom two contour corners
		approx = self.approxTarget(largestCnt)
		wpx = approx[1][0]
		hpx = approx[1][1]
		approxpoints = np.int0(cv2.boxPoints(approx))

		sortedcorners = sorted(approxpoints, key=self.getYValue)
		toptwocorners = sortedcorners[:2]
		bottomtwocorners = sortedcorners[2:]

		# Sort the corners by their x-values
		topleft, topright = sorted(toptwocorners, key=self.getXValue)
		bottomleft, bottomright = sorted(bottomtwocorners, key=self.getXValue)

		# Check if the top left point is to the left or to the right of the bottom left point
		left = topleft[0] > bottomleft[0]
		sign = 1

		# Find the two points on the side closest to the other target	
		closesttoppoint, closestbottompoint = topleft, bottomleft

		if left:
			printer.printIfNeeded("Left target", constants)
			sign = 1
			closesttoppoint = topright
			closestbottompoint = bottomright
			
		else:
			printer.printIfNeeded("Right target", constants)
			sign = -1
			closesttoppoint = topleft
			closestbottompoint = bottomleft

		# Find the distance between the closest points, which is also equal to 5.5/4 times the distance from one of the corners to the center
		# By adding (or subtracting) 4/5.5 times this distance to cx (see below), we can determine where the middle of the two targets is, even if only one is visible
		# We always calculate this distance between the closest points because the chance that they'll be cut off at the edge of the frame is unlikely, so our results will be more accurate
		# We also use this value as the height of the contour for distance calculations, which is why it's named hpx

		# Check if there's only one contour
		if len(contours) == 1:
			onecnt = True
			
			# Find cx (the horizontal center that the robot's trying to drive to) based on the detected corner and distance
			cx = closesttoppoint[0]
			cy = closesttoppoint[1]

			cx += sign*hpx*4/5.5
			
			printer.printIfNeeded("cx: " + str(cx), constants)
			printer.printIfNeeded("cy: " + str(cy), constants)

			# Draw the closest detected corner and the point in the middle of the two targets
			cv2.circle(img, (int(cx), cy), 1, (255, 0, 0), -1)
			cv2.circle(img, tuple(closesttoppoint), 5, (255, 0, 0), -1)

		else:
			# Find the centroid's coordinates
			centerxsum = centerysum = numcoords = 0.0
			for cnt in contours:
				cntcoords = image.getContourCentroidCoords(cnt)
				if cntcoords == None:
					continue
				centerxsum += cntcoords[0]
				centerysum += cntcoords[1]
				numcoords += 1
			
			cx = centerxsum / numcoords
			cy = centerysum / numcoords

		# Print out information
		distance = image_proc.getDistance(imghpx, TARGET_HEIGHT_CM, hpx, constants.getValue("viewangle"))
		angle = image_proc.getHorizAngle(imgwpx, TARGET_HEIGHT_CM, distance, hpx, cx)
		#doextake = abs(angle) < 0.087
		doextake = distance < 50

		if constants.getValue("printdata"):
			updater.printData(angle, distance, doextake, constants)
		if constants.getValue("senddata"):
			networking.sendData(constants, angle, distance, doextake, True)
		return doextake
	
	# Returns a polygonal approximation of the specified target.
	def approxTarget(self, contour):
		return cv2.minAreaRect(contour)
	# Returns the x-value of the given point for sorting.
	def getXValue(self, point):
		return point[0]

	# Returns the y-value of the given point for sorting.
	def getYValue(self, point):
		return point[1]

	# Returns the distance between the two points.
	def getDistance(self, pointA, pointB):
		return ((pointA[0] - pointB[0])**2 + (pointA[1] - pointB[1])**2)**0.5

