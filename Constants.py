import image # Custom library
'''
A class that holds different constants and global variables.
'''
class Constants:
	def __init__(self, filename):
                self.readFromFile(filename)
		self.camera = camera = image.initCamera((int(self.values["imgwpx"]), int(self.values["imghpx"]))) # Initialize the camera.
		self.viewangle = self.values["viewangle"] # The camera's viewangle.
		self.images = ["calibration/green_60cm_20deg", "calibration/green_90cm_20deg", "calibration/green_120cm_20deg", "calibration/green_60cm_10deg", "calibration/green_90cm_10deg", "calibration/green_120cm_10deg"] # The images to process.
		#self.images = ["no-targets-found.jpg", "pegclose.jpg", "waamv/orig0.jpg", "waamv/orig1.jpg", "waamv/orig2.jpg", "waamv/orig3.jpg", "waamv/orig4.jpg", "orig.jpg"]
                self.imgwpx, self.imghpx = self.camera.resolution # Image resolution.
        def readFromFile(self, filename):
                self.values = {}
                with open(filename, "r") as f:
                        for line in f:
                                spl = line.split("=")
                                self.values[spl[0]] = spl[1][:-1]
