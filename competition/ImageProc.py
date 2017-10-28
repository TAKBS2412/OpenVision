import cv2
import numpy as np
import image # Custom library

'''
A class that finds targets in an image.
'''
class ImageProc:
	# Returns None if there was an error.
	# Otherwise, returns the two contours that will be used.
	def procImage(self, img, constants):
		contours = image.getSecondLargestContour(img)
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
