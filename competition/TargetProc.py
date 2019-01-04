import cv2
import image # Custom library
import image_proc # Another custom library

'''
A class that processes targets.
'''
class TargetProc:
	# Calculates the distance, angle, and height to width ratio of the specified contour.
	def procTarget(self, constants, contours, updater, networking):
                if len(contours) == 1:
                        largestCnt = contours[0]
                else: 
        		largestCnt, secondLargestCnt = contours

		_x, _y, wpx, hpx = cv2.boundingRect(largestCnt)
						
		# Find the centroid's coordinates
		cntcoords = image.getContourCentroidCoords(largestCnt)
                if len(contours) == 2:
		        cnt2coords = image.getContourCentroidCoords(secondLargestCnt)
		        if cnt2coords == None:
		        	pass
		if cntcoords == None:
			pass
		else:
			cx, cy = cntcoords
                        pegx = cx
                        if len(contours) == 2:
			        cx2, cy2 = cnt2coords
			        pegx = (cx + cx2) / 2 # Find the x-coord of the peg (the average of the x-coordinates of the two vision targets)
			# Print out information
			distance = image_proc.getDistance(constants.getValue("imghpx"), 5.08, hpx, constants.getValue("viewangle"))
			angle = image_proc.getHorizAngle(constants.getValue("imgwpx"), 5.08, distance, hpx, pegx)
			ratio = float(hpx)/float(wpx)
			doextake = ratio < 2
			if constants.getValue("printdata"):
				updater.printData(ratio, angle, distance, doextake)
			if constants.getValue("senddata"):
				networking.sendData(angle, distance, doextake, True)
		return doextake
	
	# Returns a polygonal approximation of the specified target.
	def approxTarget(self, contour):
		x, y, w, h = cv2.boundingRect(contour)
		print("Width: " + str(w))
		return cv2.approxPolyDP(contour, 0.05*cv2.arcLength(contour, True), True)
