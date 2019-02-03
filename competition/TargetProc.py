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
			# Approximate a line running through the contours to find the angle of the contours.
			vx, vy, _cx, _cy = cv2.fitLine(largestCnt, cv2.DIST_L2, 0, 0.01, 0.01)
			vproduct = vx * vy
			left = vproduct < 0
			sign = 1
			if left:
				print("Left target")
				sign = 1
			else:
				print("Right target")
				sign = -1

			# Find the top two contour corners
			sortedcorners = sorted(approx, key=self.getYValue)[:2]

			# Fnd the distance between the two points, which is also equal to half the distance from one of the corners to the center
			# By adding (or subtracting) twice this distance to cx (wee below), we can determine where the middle of the two targets is, even if only one is visible
			distance = ((sortedcorners[1][0][0] - sortedcorners[0][0][0])**2 + (sortedcorners[1][0][1] - sortedcorners[0][0][1])**2)**0.5

			# Find the left or rightmost point on the target
			sortedcorners = sorted(sortedcorners, key=self.getXValue, reverse=left)

			# Find cx (the horizontal center that the robot's trying to drive to) based on the detected corner and distance
			cx = sortedcorners[0][0][0]
			cy = sortedcorners[0][0][1]

			cx += sign*distance*2
			
			print("cx: " + str(cx))
			print("cy: " + str(cy))

			# Draw the highest detected corners and the point in the middle of the two targets
			cv2.circle(img, (int(cx), cy), 1, (255, 0, 0), -1)
			cv2.circle(img, tuple(sortedcorners[0][0]), 5, (255, 0, 0), -1)
			cv2.circle(img, tuple(sortedcorners[1][0]), 1, (255, 0, 0), -1)

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
