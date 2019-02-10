import datetime
import printer
''' Calculates the FPS based on the number of frames processed over time. '''
class FPS:
	def __init__(self):
		self.framesprocessed = 0.0
		self.starttime = datetime.datetime.now()

	def update(self, constants):
		self.framesprocessed += 1
		self.elapsedtime = datetime.datetime.now() - self.starttime
		self.fps = self.framesprocessed / self.elapsedtime.total_seconds()
		
		printer.printIfNeeded("FPS: " + str(self.fps), constants)
