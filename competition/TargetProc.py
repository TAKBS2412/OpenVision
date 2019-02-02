import cv2
import image # Custom library
import image_proc # Another custom library

'''
A class that processes targets.
'''
class TargetProc:
	# Calculates the distance, angle, and height to width ratio of the specified contour.
	def procTarget(self, constants, contours, updater, networking):
		largestCnt = contours[0]

		# Check if there's only one contour
		if len(contours) == 1:
			# Approximate a line running through the contours to find the angle of the contours.
			vx, vy, cx, cy = cv2.fitLine(largestCnt, cv2.DIST_L2, 0, 0.01, 0.01)
			vproduct = vx * vy
			if vproduct > 0:
				print("Right target")
			else:
				print("Left target")

		_x, _y, wpx, hpx = cv2.boundingRect(largestCnt)
						
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
		distance = image_proc.getDistance(constants.getValue("imghpx"), 5.08, hpx, constants.getValue("viewangle"))
		angle = image_proc.getHorizAngle(constants.getValue("imgwpx"), 5.08, distance, hpx, cx)
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
