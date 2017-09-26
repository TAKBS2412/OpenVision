import numpy as np
import cv2
import glob

width = 9
height = 6

# Arrays to store object points and image points from all the images.
objpoints = np.array([
	[0, 0, 0], # Bottom right corner
	[2, 0, 0], # Bottom left corner
	[2, 5, 0], # Top left corner
	[0, 5, 0]  # Top right corner
], np.float32) # 3d points in real world space
imgpoints = np.array([
	[0, 0], # Bottom right corner
	[2, 0], # Bottom left corner
	[2, 5], # Top left corner
	[0, 5]  # Top right corner
], np.float32) # 2d points in image plane.

'''
imgpoints = np.array([
	[468, 215], # Bottom right corner
	[439, 215], # Bottom left corner
	[435, 144], # Top left corner
	[464, 144] # Top right corner

], np.float32) # 2d points in image plane.
fname = '/home/pi/src/calibration/green_90cm_20deg'

img = cv2.imread(fname)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
'''

'''
mtx = np.array([[ 1022.22975169,    0,          323.13447241],
	[   0,          1155.02013658,   232.738004 ],
	[   0,            0,            1,        ]])
'''
mtx = np.array([[ 1,    0,          1],
	[   0,          1,   1 ],
	[   0,            0,            1,        ]])

#dist = np.array([[  0.602425468,   3.12143930,   0.00222685358,   0.00122617243, -161.215092]])
dist = np.array([[  0,   0,   0,   0, 0]])


ret, rvec, tvec = cv2.solvePnP(objpoints, imgpoints, mtx, dist)
print("ret: {}".format(ret))
print("rvec: {}".format(rvec))
print("tvec: {}".format(tvec))

print("")
rodrvec, jacobian = cv2.Rodrigues(rvec)
print("rodrvec: {}".format(rodrvec))

'''
projmtx = np.array([
	[rodrvec[0], rodrvec[1], rodrvec[2], 0],
	[rodrvec[3], rodrvec[4], rodrvec[5], 0],
	[rodrvec[6], rodrvec[7], rodrvec[8], 0]
], np.float32)
'''
zeros = np.array([[0, 0, 0]], np.float32)
projmtx = np.concatenate((rodrvec, zeros.T), axis=1)
print("projmtx: {}".format(projmtx))
cammtx, rotmtx, transvect, rotmtxx, rotmtxy, rotmtxz, eulerangles = cv2.decomposeProjectionMatrix(projmtx)

print("")

print("cammtx: {}".format(cammtx))
print("rotmtx: {}".format(rotmtx))
print("transvect: {}".format(transvect))
print("rotmtxx: {}".format(rotmtxx))
print("rotmtxy: {}".format(rotmtxy))
print("rotmtxz: {}".format(rotmtxz))
print("eulerangles: {}".format(eulerangles))

cv2.destroyAllWindows()
