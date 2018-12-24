import cv2
import numpy as np
import image # Custom library

'''
A class that finds targets in an image.
'''
class ImageProc:
	# Finds all the contours in the image iamge and sorts them by size (largest to smallest)
	# Returns an array of the sorted contours. If no contours have been found, returns an empty array
	def sortContours(self, image):
		# Find contours
		image, contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)

		# If no contours have been found, quit
		if len(contours) == 0:
			#sys.exit("Error: No targets found!")
			return []
		
		return sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

	# Checks the contour to make sure it fulfills the requirements (nonzero size, rectangular, etc.)
	# The parameter funcs is an array of functions that checks each contour
	def checkContour(self, cnt, funcs):
		'''
		cntArea = cv2.contourArea(cnt)
		approx = cv2.approxPolyDP(cnt, 0.05*cv2.arcLength(cnt, True), True)
		if len(approx) != 4: return False # Make sure the contour's rectangular

		polygonArea = cv2.contourArea(approx)
		if polygonArea == 0 or cntArea == 0: return False # Make sure the contour has a nonzero area
		percentFilled = polygonArea/cntArea*100
		if percentFilled < 70: return False # Make sure the contour is filled
		'''
		for func in funcs:
			if not func(cnt): return False
		return True

	# Checks if the contour cnt has a nonzero area
	# Returns True if cnt's area is not equal to zero
	def isContourEmpty(self, cnt):
		cntArea = cv2.contourArea(cnt)
		approx = cv2.approxPolyDP(cnt, 0.05*cv2.arcLength(cnt, True), True)

		polygonArea = cv2.contourArea(approx)
		return polygonArea != 0 and cntArea != 0

	# Checks if the contour is rectangular
	def isContourRectangular(self, cnt):
		approx = cv2.approxPolyDP(cnt, 0.05*cv2.arcLength(cnt, True), True)
		return len(approx) == 4

	# Checks how filled the contour is
	def isContourFilled(self, cnt):
		cntArea = cv2.contourArea(cnt)
		approx = cv2.approxPolyDP(cnt, 0.05*cv2.arcLength(cnt, True), True)

		polygonArea = cv2.contourArea(approx)
		percentFilled = polygonArea/cntArea*100
		return percentFilled > 70

	# Finds the largest and second-largest contour in the processed image
	# image - the HSV-filtered image to process
	# Returns None if no targets were found
	# Otherwise, returns an array - the first element is the largest contour, the second is the second-largest contour
	def getSecondLargestContour(self, image):
		# Find contours
		#image, contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)

		# Find sorted list of contours
		contours = self.sortContours(image)
		
		# If no contours have been found, quit
		if len(contours) == 0:
			#sys.exit("Error: No targets found!")
			return None

		# Filter the list based on checkContour()
		funcs = [self.isContourEmpty, self.isContourRectangular, self.isContourFilled]
		filteredcontours = [cnt for cnt in contours if self.checkContour(cnt, funcs)]

		return filteredcontours[:2]

	# Returns None if there was an error.
	# Otherwise, returns the two contours that will be used.
	def procImage(self, img, constants):
		contours = self.getSecondLargestContour(img)
		if contours is None:
			return None
		largestCnt, secondLargestCnt = contours
		if largestCnt is None and secondLargestCnt is None:
			return None
		contours2 = []
		for cnt in contours:
			if cnt != None:
				contours2.append(cnt)
		return contours2
