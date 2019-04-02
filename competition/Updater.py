import cv2
import datetime
import printer
'''
This class displays the GUI and prints/logs data, depending on the settings in Constants.
'''
class Updater:
	# Returns the current date and time as a string.
	def getDateTime(self):
		return str(datetime.datetime.now()).replace(" ", "_")

	# Finds the folder and date to use as a file name prefix
	def getFilePrefix(self):
		return "pncmp/" + self.getDateTime() + "-"

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
	def printData(self, angle, distance, doextake, constants):
		printer.printIfNeeded("Angle: " + str(angle), constants)
		printer.printIfNeeded("Distance: " + str(distance), constants)
		printer.printIfNeeded("Should Extake: " + str(doextake), constants)

	# Sends data using NetworkTables.
	# DEPRECATED: Use Networking.sendDataNT() function instead
	def sendData(self, sd, angle, distance, doextake, targetsFound):
		# Send the variables to the roboRIO
		sd.putNumber("angle", angle)
		sd.putNumber("distance", distance)
		sd.putBoolean("doextake", doextake) 
		sd.putBoolean("targetsFound", targetsFound)

	# Prints out the HSV values for filtering
	def printHSV(self, constants):
		printer.printIfNeededHSV("Upper HSV: " + str(constants.getValue("higherh")) + ", " + str(constants.getValue("highers")) + ", " + str(constants.getValue("higherv")), constants)
		printer.printIfNeededHSV("Lower HSV: " + str(constants.getValue("lowerh")) + ", " + str(constants.getValue("lowers")) + ", " + str(constants.getValue("lowerv")), constants)

	# Called when the images have been written.
	def imgWritten(self, constants):
		printer.printIfNeeded("Images written.", constants)

	# Called when no contours have been found.
	def contoursNotFound(self, constants, img, oldimg):
		if constants.getValue("printdata"):
			printer.printIfNeeded("Contours not found!", constants)
		if not constants.getValue("imagesaved"):
			cv2.imwrite(self.getFilePrefix() + "no-targets-found.jpg", oldimg)
			cv2.imwrite(self.getFilePrefix() + "no-targets-found-proc.jpg", img)
			constants.setValue("imagesaved", True)
	# Called when the peg is close.
	def doextake(self, constants, img, oldimg):
		if not constants.getValue("imagesaved"):
			cv2.imwrite(self.getFilePrefix() + "doextake.jpg", oldimg)
			cv2.imwrite(self.getFilePrefix() + "doextake-proc.jpg", img)
			constants.setValue("imagesaved", True)
