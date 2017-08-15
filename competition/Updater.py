import cv2
'''
This class displays the GUI and prints/logs data, depending on the settings in Constants.
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
	def printData(self, ratio, angle, distance, pegclose):
		print("Ratio: " + str(ratio))
		print("Angle: " + str(angle))
		print("Distance: " + str(distance))
		print("Peg close: " + str(pegclose))

	# Sends data using NetworkTables.
	def sendData(self, sd, angle, distance, pegclose, targetsFound):
		# Send the variables to the roboRIO
		sd.putNumber("angle", angle)
		sd.putNumber("distance", distance)
		sd.putBoolean("pegclose", pegclose) 
		sd.putBoolean("targetsFound", targetsFound)


	# Prints out the HSV values for filtering
	def printHSV(self, constants):
		print("Upper HSV: " + str(constants.getValue("higherh")) + ", " + str(constants.getValue("highers")) + ", " + str(constants.getValue("higherv")))
		print("Lower HSV: " + str(constants.getValue("lowerh")) + ", " + str(constants.getValue("lowers")) + ", " + str(constants.getValue("lowerv")))

	# Called when the images have been written.
	def imgWritten(self):
		print("Images written.")

	# Called when no contours have been found.
	def contoursNotFound(self, constants, img, oldimg):
		print("Contours not found!")
		if not constants.getValue("imagesaved"):
			cv2.imwrite("no-targets-found.jpg", oldimg)
			cv2.imwrite("no-targets-found-proc.jpg", img)
			constants.setValue("imagesaved", True)
	# Called when the peg is close.
	def pegclose(self, constants, img, oldimg):
		if not constants.getValue("imagesaved"):
			cv2.imwrite("pegclose.jpg", oldimg)
			cv2.imwrite("pegclose-proc.jpg", img)
			constants.setValue("imagesaved", True)
