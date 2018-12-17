import PiVideoStream
import time
import FPS
import cv2

vs = PiVideoStream.PiVideoStream().start()
time.sleep(2.0)

# FPS tracker
fps = FPS.FPS()

key = "1"
while not key == ord("q"):
	frame = vs.read()
	cv2.imshow("Frame", frame)
	fps.update(True)
	
	key = cv2.waitKey(1)

cv2.destroyAllWindows()	
vs.stop()
