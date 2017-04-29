import numpy as np
import cv2

'''
An example of a SURF based matcher.
'''

img1 = cv2.imread('pegclose.jpg',0)	 # queryImage
img2 = cv2.imread('green_targets.jpg',0) # trainImage

# Initiate SURF detector
surf = cv2.xfeatures2d.SURF_create()

# Find the keypoints and descriptors with SURF
kp1, des1 = surf.detectAndCompute(img1,None)
kp2, des2 = surf.detectAndCompute(img2,None)

# BFMatcher with default params
bf = cv2.BFMatcher()
#matches = bf.knnMatch(des1, des2, k=2)
matches = bf.knnMatch(des1, des2, k=2)
# store all the good matches as per Lowe's ratio test.
good = []
for m,n in matches:
	#if m.distance < 0.7*n.distance:
	good.append(m)

img3 = None
img3 = cv2.drawMatches(img1,kp1,img2,kp2,good, img3, flags=2)
cv2.imshow("Matches", img3)
cv2.waitKey(0)
