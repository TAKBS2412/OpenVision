import numpy as np
import cv2

'''
Some assorted functions that find points, order them, and process them.
'''


# Finds the points from a rotated rectangle (such as one returned from cv2.minAreaRect())
# Returns an array of points, which can be passed to find_straight_rect()

def find_points(rect):
	# The center is the first tuple in rect,
	# the width and height the second tuple,
	# and the last number the angle

	center = rect[0]
	width, height = rect[1]
	angle = np.radians(rect[2])

	# Find the actual (non-rotated) width and height
	actualwidth = np.cos(angle) * width
	actualheight = np.cos(angle) * height 

	# Find the points from the actual width and height
	actualwidth_half = actualwidth / 2
	actualheight_half = actualheight / 2
	topleft = (center[0] - actualwidth_half, center[1] - actualheight_half)
	topright = (center[0] + actualwidth_half, center[1] - actualheight_half)
	bottomleft = (center[0] - actualwidth_half, center[1] + actualheight_half)
	bottomright = (center[0] + actualwidth_half, center[1] + actualheight_half)

	# Return the points
	return np.array([
		topleft, topright, bottomright, bottomleft
	], dtype = "float32")

# See http://www.pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/
#
# Given an array of points, finds a "straightened" rectangle (represented as an array of points)

def find_straight_rect(pts):
	rect = order_points(pts)
	(tl, tr, br, bl) = rect

	# Find the width of the new rectangle
	widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
	widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
	maxWidth = max(int(widthA), int(widthB)) - 1

	# Find the height of the new image
	heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
	heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
	maxHeight = max(int(heightA), int(heightB)) - 1

	# Use the top-left corner to compute the rest of the rectangle
	straightrect = np.array([
		tl,
		[tl[0] + maxWidth, tl[1]],
		[tl[0] + maxWidth, tl[1] + maxHeight],
		[tl[0], tl[1] + maxHeight]
	], dtype = "float32")

	# Return the straightened rectangle
	return straightrect

# See http://www.pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/
# 
# Orders the array of points pts
# So that the first entry is the top left,
# the second is top right,
# the third is bottom right,
# and the fourth is bottom left

def order_points(pts):
	rect = np.zeros((4, 2), dtype = "float32")

	# The top-left point will have the smallest sum, but the bottom right will have the largest
	s = pts.sum(axis = 1)
	rect[0] = pts[np.argmin(s)]
	rect[2] = pts[np.argmax(s)]

	# Compute the difference between the points
	# Top-right will have the lowest difference, while bottom-left will have the highest
	diff = np.diff(pts, axis = 1)
	rect[1] = pts[np.argmin(diff)]
	rect[3] = pts[np.argmax(diff)]

	# Return the ordered coordinates
	return rect
