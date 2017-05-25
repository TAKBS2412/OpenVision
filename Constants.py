import image # Custom library
'''
A class that holds different constants and global variables.
'''
class Constants:
	def __init__(self):
		self.initialize()
	def initialize(self):
		self.camera = camera = image.initCamera((640, 480)) # Initialize the camera.
		self.viewangle = 0.726 # The camera's viewangle.
		self.images = ["calibration/green_60cm_20deg", "calibration/green_90cm_20deg", "calibration/green_120cm_20deg", "calibration/green_60cm_10deg", "calibration/green_90cm_10deg", "calibration/green_120cm_10deg"] # The images to process.
		#self.images = ["no-targets-found.jpg", "pegclose.jpg", "waamv/orig0.jpg", "waamv/orig1.jpg", "waamv/orig2.jpg", "waamv/orig3.jpg", "waamv/orig4.jpg", "orig.jpg"]
