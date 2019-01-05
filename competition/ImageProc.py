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
		self.cntArea = cv2.contourArea(cnt)
		self.approx = cv2.approxPolyDP(cnt, 0.05*cv2.arcLength(cnt, True), True)
		self.polygonArea = cv2.contourArea(self.approx)
		
		for func in funcs:
			if not func(cnt): return False
		return True

	# Checks if the contour cnt has a nonzero area
	# Returns True if cnt's area is not equal to zero
	def isContourEmpty(self, cnt):
		return self.polygonArea != 0 and self.cntArea != 0

	# Checks if the contour is rectangular
	def isContourRectangular(self, cnt):
		return len(self.approx) == 4

	# Checks how filled the contour is
	def isContourFilled(self, cnt):
		percentFilled = self.polygonArea/self.cntArea*100
		return percentFilled > 70

	# Finds the top num largest contours in the processed image
	# image - the HSV-filtered image to process
	# num - the number of contours to find
	# Returns None if no targets were found
	# Otherwise, returns an array - the first element is the largest contour, the second is the second-largest contour
	def getNumLargestContours(self, image, num):
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

		return filteredcontours[:num]

	# Returns None if there was an error.
	# Otherwise, returns the two contours that will be used.
	def procImage(self, img, constants):
		numcontours = 2
		contours = self.getNumLargestContours(img, numcontours)
		if contours is None: return contours
		return [cnt for cnt in contours]

