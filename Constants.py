import ast
import image # Custom library
'''
A class that holds different constants and global variables.
'''
class Constants:
	def __init__(self, filename):
                self.readFromFile(filename)
		self.camera = camera = image.initCamera((self.values["imgwpx"], self.values["imghpx"])) # Initialize the camera.
                self.imgwpx, self.imghpx = self.camera.resolution # Image resolution.
        def readFromFile(self, filename):
                self.values = {}
                with open(filename, "r") as f:
                        for line in f:
                                spl = line.split("=")
                                self.values[spl[0]] = ast.literal_eval(spl[1][:-1])
        def getValue(self, constantname):
                return self.values[constantname]
