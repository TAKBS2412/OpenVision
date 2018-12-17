'''Threaded class that allows us to read camera frames faster.
 See https://www.pyimagesearch.com/2015/12/28/increasing-raspberry-pi-fps-with-python-and-opencv/'''
from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Thread
import cv2

class PiVideoStream:
	def __init__(self, resolution=(640, 480), framerate=32):
		# Initialize the camera and stream
		self.camera = PiCamera()
		self.camera.resolution = resolution
		self.camera.framerate = framerate
		self.rawCapture = PiRGBArray(self.camera, size=resolution)
		self.stream = self.camera.capture_continuous(self.rawCapture,
			format="bgr", use_video_port=True)
 
		# Initialize the frame and the variable used to indicate
		# if the thread should be stopped
		self.frame = None
		self.stopped = False
	def start(self):
		# Start the thread to read frames from the video stream
		Thread(target=self.update, args=()).start()
		return self
 
	def update(self):
		# Keep looping infinitely until the thread is stopped
		for f in self.stream:
			# Grab the frame from the stream and clear the stream in
			# Preparation for the next frame
			self.frame = f.array
			self.rawCapture.truncate(0)
 
			# If the thread indicator variable is set, stop the thread
			# and resource camera resources
			if self.stopped:
				self.stream.close()
				self.rawCapture.close()
				self.camera.close()
				return
	def read(self):
		# Return the frame most recently read
		return self.frame
 
	def stop(self):
		# Indicate that the thread should be stopped
		self.stopped = True
