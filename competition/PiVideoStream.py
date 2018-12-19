'''Threaded class that allows us to read camera frames faster.
 See https://www.pyimagesearch.com/2015/12/28/increasing-raspberry-pi-fps-with-python-and-opencv/'''
from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
import cv2
import ImageFiltering

class PiVideoStream:
	def __init__(self, constants, resolution=(640, 480), framerate=32):
		# Store the constants
		self.constants = constants

		# Initialize the camera and stream
		self.camera = PiCamera()
		self.camera.resolution = resolution
		self.camera.framerate = framerate
		self.rawCapture = PiRGBArray(self.camera, size=resolution)
		self.stream = self.camera.capture_continuous(self.rawCapture,
			format="bgr", use_video_port=True)

		# Initialize the frames and the variable used to indicate
		# if the thread should be stopped
		self.frames = [None] * 2 # The array has two elements (the old fraem and the new frame)
		self.stopped = False
		
		# Initialize the class used for filtering the frame
		self.imagefilter = ImageFiltering.ImageFiltering()
	def start(self):
		# Start the thread to read frames from the video stream
		Thread(target=self.update, args=()).start()
		return self
	def update(self):
		# Keep looping infinitely until the thread is stopped
		for f in self.stream:
			# Grab the frame from the stream and clear the stream in
			# Preparation for the next frame
			self.frames[0] = f.array
			self.rawCapture.truncate(0)

			# Filter the frame and store the processed version
 			self.frames[1] = self.imagefilter.filterImage(self.frames[0], self.constants)

			# If the thread indicator variable is set, stop the thread
			# and resource camera resources
			if self.stopped:
				self.stream.close()
				self.rawCapture.close()
				self.camera.close()
				return
	def read(self):
		# Return the frames most recently read
		return self.frames
 
	def stop(self):
		# Indicate that the thread should be stopped
		self.stopped = True
