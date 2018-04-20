import numpy as np
import cv2
import argparse
# USAGE: python2 contours.py -i"./ostracod.png" -b120 -w120
# The above params work pretty well

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
    help="path to input image")
ap.add_argument("-b", "--black", required=True, type=int,
    help="threshold below which is black above which is white")
ap.add_argument("-w", "--white", required=True, type=int,
    help="pixels above the threshold will have this value")
args = vars(ap.parse_args())
black = args["black"]
white = args["white"]

im = cv2.imread(args["image"])

imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)

ret,thresh = cv2.threshold(imgray,black,white,cv2.THRESH_BINARY)
imgray, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
cv2.imshow("imgray",imgray)
cv2.waitKey(0)

print "X\tY\tArea\tMinI\tMaxI\tMeanI"
for c in contours:
    # compute the center of the contour
    if cv2.contourArea(c) > 0:
        M = cv2.moments(c)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        mask = np.zeros(imgray.shape,np.uint8)
        cv2.drawContours(mask,[c],0,255,-1)
        mean_val = cv2.mean(im,mask = mask)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(imgray,mask = mask)
        print cX,"\t",cY,"\t",cv2.contourArea(c),"\t",min_val,"\t",max_val,"\t",mean_val[0]

cv2.drawContours(im,contours,-1,(0,255,0),-1)
cv2.imshow("Contours", im)
cv2.waitKey(0)

