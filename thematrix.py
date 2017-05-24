import numpy as np
import cv2
'''
This script calculates the skew using matrices.
'''

# 180 degree rotation
orig = np.array([[1, -1, 0], [4, -1, 0], [4, -3, 0], [1, -3, 0]], np.float32)
dst = np.array([[1, -1], [4, -1], [4, -3], [1, -3]], np.float32)

#s = np.array([[1288.28889, 0, 74.5903466], [0, 1291.14257, 153.495243], [0, 0, 1]])
s = np.array([[1, 0, 1], [0, 1, 1], [0, 0, 1]])
retval, rvec, tvec = cv2.solvePnP(orig, dst, s, None)

rmat = cv2.Rodrigues(rvec)[0]

projmat = np.empty([3, 4])
for r in rmat:
	np.append(r, 0)
	np.append(projmat, r)
dematrix = cv2.decomposeProjectionMatrix(projmat)
print(rvec)
print("")
print(dematrix[3])
print(dematrix[4])
print(dematrix[5])
print("")
print(dematrix[6])
