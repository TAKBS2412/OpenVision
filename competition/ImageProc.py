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

	# Checks the contour to make sure it fulfills the requirements (nonzero size, etc.)
	# The parameter funcs is an array of functions that checks each contour
	def checkContour(self, cnt, funcs):
		self.cntArea = cv2.contourArea(cnt)
		arclength = cv2.arcLength(cnt, True)

		self.rect = cv2.minAreaRect(cnt)

		width = self.rect[1][0]
		height = self.rect[1][1]
		print(self.rect)
		print(width)
		print(height)
		self.rectArea = width*height

		for func in funcs:
			if not func(cnt): return False
		return True

	# Checks if the contour cnt has a nonzero area
	# Returns True if cnt's area is not equal to zero
	def isContourEmpty(self, cnt):
		return self.rectArea != 0 and self.cntArea != 0

	# Checks how filled the contour is
	def isContourFilled(self, cnt):
		percentFilled = self.rectArea/self.cntArea*100
		print("Filled %: " + str(percentFilled))

		return 100 < percentFilled < 130

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
		#funcs = [self.isContourEmpty, self.isContourRectangular]
		funcs = [self.isContourEmpty]
		filteredcontours = [cnt for cnt in contours if self.checkContour(cnt, funcs)]

		#return filteredcontours[:num]
		return filteredcontours

	# Returns None if there was an error.
	# Otherwise, returns the two contours that will be used.
	def procImage(self, img, constants):
		numcontours = 2
		contours = self.getNumLargestContours(img, numcontours)
		if contours is None: return contours
		return [cnt for cnt in contours]

