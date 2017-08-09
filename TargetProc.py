import cv2
import image # Custom library
import image_proc # Another custom library

'''
A class that processes targets.
'''
class TargetProc:
	def procTarget(self, constants, contours):
		largestCnt, secondLargestCnt = contours

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


