import cv2
'''
This class displays the GUI (test_video.py only) and prints/logs data.
'''
class Updater:
	# Updates the GUI.
	def updateGUI(self, constants, img, oldimg):
		# Show the original and processed frames
		oldimgname = constants.getValue("images")[constants.getValue("index")]
		if constants.getValue("usevideo"):
			oldimgname = "Live camera feed"
		cv2.imshow(oldimgname, oldimg)
		cv2.imshow("Processed Frame", img)

		if constants.getValue("lastoldimgname") and constants.getValue("lastoldimgname") != oldimgname:
			cv2.destroyWindow(constants.getValue("lastoldimgname"))
		constants.setValue("lastoldimgname", oldimgname)
	# Prints data.
	def printData(self, cx, cy, hpx, wpx, distance, angle):
		print("Ratio: " + str(hpx/wpx))
		print("Centroid coordinates: (" + str(cx) + ", " + str(cy) + ")")
		print("Height (px): " + str(hpx))
		print("Width (px): " + str(wpx))
		print("Distance (cm): " + str(distance))
		print("Angle (radians): " + str(angle))

	# Prints out the HSV values for filtering
	def printHSV(self, constants):
		print("Upper HSV: " + str(constants.getValue("higherh")) + ", " + str(constants.getValue("highers")) + ", " + str(constants.getValue("higherv")))
		print("Lower HSV: " + str(constants.getValue("lowerh")) + ", " + str(constants.getValue("lowers")) + ", " + str(constants.getValue("lowerv")))

	# Called when the images have been written.
	def imgWritten(self):
		print("Images written.")

	# Called when no contours have been found.
	def contoursNotFound(self):
		print("Contours not found!")
