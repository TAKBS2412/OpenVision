import cv2
import numpy as np
import printer

'''
A class that prepares and filters an image.
'''
class ImageFiltering:
	def filterImage(self, img, constants):
		# Check if the image is None first
		if img is None:
			printer.printIfNeeded("Error: Image is empty!", constants)
		else:
			# Blur the image
			img = cv2.GaussianBlur(img, (5, 5), 0)
			
			# HSV filter the image
			img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
			lower_range = np.array([constants.getValue("lowerh"), constants.getValue("lowers"), constants.getValue("lowerv")])
			higher_range = np.array([constants.getValue("higherh"), constants.getValue("highers"), constants.getValue("higherv")])
			HSVmask = cv2.inRange(img, lower_range, higher_range)
			img = cv2.bitwise_and(img, img, mask=HSVmask)
			img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

		return img
