import numpy as np
import cv2
import matplotlib as plt

'''
An example of Brute-Force Matching with ORB Descriptors (faster than SIFT).
See docs.opencv.org/trunk/dc/dc3/tutorial_py_matcher.html
'''

img1 = cv2.imread('test.jpg',0)	   # queryImage
img2 = cv2.imread('cropped.jpg',0) # trainImage

# Initiate ORB detector
orb = cv2.ORB_create()

# find the keypoints and descriptors with ORB
kp1, des1 = orb.detectAndCompute(img1,None)
kp2, des2 = orb.detectAndCompute(img2,None)

# Create BFMatcher object
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

# Match descriptors.
matches = bf.match(des1,des2)

# Sort them in the order of their distance.
matches = sorted(matches, key = lambda x:x.distance)

# Draw the matches.
img3 = None
img3 = cv2.drawMatches(img1,kp1,img2,kp2,good,img3, flags=2)
cv2.imshow("Matches", img3)
cv2.waitKey(0)

