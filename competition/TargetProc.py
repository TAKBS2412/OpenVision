import cv2
import image # Custom library
import image_proc # Another custom library

'''
A class that processes targets.
'''
class TargetProc:
	# Calculates the distance, angle, and height to width ratio of the specified contour.
	def procTarget(self, constants, contours, updater, networking, approx, img):
		largestCnt = contours[0]

		approx = self.approxTarget(largestCnt)

		onecnt = False
		left = True
		offx = 8 / 2 * 2.54 # Halve the 8 inches and convert to cm

		imghpx = constants.getValue("imghpx")
		imgwpx = constants.getValue("imgwpx")

		# Make the center of the contours default to the middle of the image
		cx = imgwpx / 2.0
		cy = imghpx / 2.0

		# Calculate the height and width of the largest contour
		_x, _y, wpx, hpx = cv2.boundingRect(largestCnt)

		# Check if there's only one contour
		if len(contours) == 1:
			onecnt = True

			# Find the top two and bottom two contour corners
			sortedcorners = sorted(approx, key=self.getYValue)
			toptwocorners = sortedcorners[:2]
			bottomtwocorners = sortedcorners[2:]

			# Sort the corners by their x-values
			topleft, topright = sorted(toptwocorners, key=self.getXValue)
			bottomleft, bottomright = sorted(bottomtwocorners, key=self.getXValue)

			# Check if the top left corner is above or below the top right corner
			left = topleft[0][1] < topright[0][1]
			sign = 1
			if left:
				print("Left target")
				sign = 1
			else:
				print("Right target")
				sign = -1

			# Find the distance between the top two corners, which is also equal to half the distance from one of the corners to the center
			# By adding (or subtracting) twice this distance to cx (see below), we can determine where the middle of the two targets is, even if only one is visible
			distance = ((topleft[0][0] - topright[0][0])**2 + (topleft[0][1] - topright[0][1])**2)**0.5

			# Find the point closest to the other target
			closestpoint = topright if left else topleft

			# Find cx (the horizontal center that the robot's trying to drive to) based on the detected corner and distance
			cx = closestpoint[0][0]
			cy = closestpoint[0][1]

			cx += sign*distance*2
			
			print("cx: " + str(cx))
			print("cy: " + str(cy))

			# Draw the closest detected corner and the point in the middle of the two targets
			cv2.circle(img, (int(cx), cy), 1, (255, 0, 0), -1)
			cv2.circle(img, tuple(closestpoint[0]), 5, (255, 0, 0), -1)

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
		distance = image_proc.getDistance(imghpx, 5.08, hpx, constants.getValue("viewangle"))
		angle = image_proc.getHorizAngle(imgwpx, 5.08, distance, hpx, cx)
		doextake = abs(angle) < 0.087

		if constants.getValue("printdata"):
			updater.printData(angle, distance, doextake)
		if constants.getValue("senddata"):
			networking.sendData(constants, angle, distance, doextake, True)
		return doextake
	
	# Returns a polygonal approximation of the specified target.
	def approxTarget(self, contour):
		x, y, w, h = cv2.boundingRect(contour)
		print("Width: " + str(w))
		return cv2.approxPolyDP(contour, 0.05*cv2.arcLength(contour, True), True)

	# Returns the x-value of the given point for sorting.
	def getXValue(self, point):
		return point[0][0]

	# Returns the y-value of the given point for sorting.
	def getYValue(self, point):
		return point[0][1]
