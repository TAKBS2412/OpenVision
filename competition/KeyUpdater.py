import cv2
import datetime
'''
A class that updates constants based on which key has been pressed.
'''
class KeyUpdater:
	# Updates all of the flags/settings based on which key was pressed.
	def update(self, constants, key, updater, img, oldimg):
		if constants.getValue("tuneHSV"):
			if key == ord("u"):
				constants.setValue("adjustHigher", not constants.getValue("adjustHigher"))
			if key == ord("r"):
				constants.setValue("raiseValue", constants.getValue("raiseValue") * -1)
			if key == ord("p"):
				constants.setValue("procImage", not constants.getValue("procImage"))
			elif key == ord("h"):
				if constants.getValue("adjustHigher"):
					constants.setValue("higherh", constants.getValue("higherh") + constants.getValue("raiseValue"))
					updater.printHSV(constants)
				else:
					constants.setValue("lowerh", constants.getValue("lowerh") + constants.getValue("raiseValue"))
					updater.printHSV(constants)
			elif key == ord("s"):
				if constants.getValue("adjustHigher"):
					constants.setValue("highers", constants.getValue("highers") + constants.getValue("raiseValue"))
					updater.printHSV(constants)
				else:
					constants.setValue("lowers", constants.getValue("lowers") + constants.getValue("raiseValue"))
					updater.printHSV(constants)
			elif key == ord("v"):
				if constants.getValue("adjustHigher"):
					constants.setValue("higherv", constants.getValue("higherv") + constants.getValue("raiseValue"))
					updater.printHSV(constants)
				else:
					constants.setValue("lowerv", constants.getValue("lowerv") + constants.getValue("raiseValue"))
					updater.printHSV(constants)
		if key == ord("w"):
			# Write the image files
			filename = "/home/pi/Pictures/Camera Roll/" + str(datetime.datetime.now()).replace(" ", "_") # Use current date as filename.
			cv2.imwrite(filename + ".jpg", oldimg)
			cv2.imwrite(filename + "_proc.jpg", img)
			updater.imgWritten(constants)
		if key == ord("i"):
			# Toggle usevideo
			constants.setValue("usevideo", not constants.getValue("usevideo"))
		if key == 81:
			constants.setValue("index", constants.getValue("index") - 1 if constants.getValue("index") > 0 else len(constants.getValue("images"))-1)
		elif key == 83:
			constants.setValue("index", constants.getValue("index") + 1 if constants.getValue("index") < len(constants.getValue("images"))-1 else 0)
		if key == ord("q"):
			constants.setValue("endloop", True)


