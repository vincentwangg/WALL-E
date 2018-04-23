#!/usr/bin/env python

import numpy as np
import cv2

sift = cv2.xfeatures2d.SIFT_create()

original = cv2.imread("Undistortionresult.png")
adjusted = cv2.imread("Undistortionresult2.png")
cv2.imshow("Images", np.hstack([original, adjusted]))
cv2.waitKey(0)
