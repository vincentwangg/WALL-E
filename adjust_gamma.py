#!/usr/bin/env python

# import the necessary packages
from __future__ import print_function
import numpy as np
import argparse
import cv2

def adjust_clip(image, black=0, white=255):
	# build a lookup table mapping the pixel values [0, 255] to
	# set values below black to 0 and above white to 255
	zeros = np.array([i * 0
		for i in np.arange(0,black)]).astype("uint8")
	whites = np.array([(i * 0) + 255
		for i in np.arange(0,256-white)]).astype("uint8")
	table = np.array([i + black
		for i in np.arange(0,white-black)]).astype("uint8")
	table = np.concatenate((zeros,table,whites))
#	print("LUT for clipping mask")
#	print(table)
	return cv2.LUT(image, table)

def adjust_gamma(image, gamma=1.0):
	# build a lookup table mapping the pixel values [0, 255] to
	# their adjusted gamma values
	invGamma = 1.0 / gamma
	table = np.array([((i / 255.0) ** invGamma) * 255
		for i in np.arange(0, 256)]).astype("uint8")
	# apply gamma correction using the lookup table
#	print(table)
	return cv2.LUT(image, table)

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image")
ap.add_argument("-g", "--gamma", required=True, type=float,
	help="value of gamma")
ap.add_argument("-b", "--black", required=True, type=int,
	help="threshold below which is black")
ap.add_argument("-w", "--white", required=True, type=int,
	help="threshold above which is white")
args = vars(ap.parse_args())
gamma = args["gamma"]
black = args["black"]
white = args["white"]


# load the original image
original = cv2.imread(args["image"])
clipped = adjust_clip(original, black=black, white=white)
gamma = gamma if gamma > 0 else 0.1
adjusted = adjust_gamma(clipped, gamma=gamma)
cv2.imshow("Images", np.hstack([original, adjusted]))
cv2.imwrite("TEST.png",adjusted)
cv2.waitKey(0)
