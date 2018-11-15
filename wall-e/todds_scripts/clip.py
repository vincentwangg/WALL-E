#!/usr/bin/env python

import numpy as np
import cv2
import argparse
import time

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--path", required=False, default='.', 
        help="path to video frame files default is ./")
ap.add_argument("-v1", "--video1", required=True, type=str,
	help="file name for first video")
ap.add_argument("-v2", "--video2", required=True, type=str,
	help="filename for second video")
ap.add_argument("-s", "--start", required=False, default=1, type=int,
	help="frame to start at default = 1")
ap.add_argument("-e", "--endframe", required=False, default=0, type=int,
	help="frame to end default (0) = play to end")
ap.add_argument("-o", "--offset", required=False, default=0, type=int,
	help="number of frames to offset two videos, positive or negative")
ap.add_argument("-d", "--delay", required=False, default=0, type=float,
	help="delay time between frames for slo-mo")
args = vars(ap.parse_args())
offset = args["offset"]
delay = args["delay"]
start = args["start"]
endframe = args["endframe"]
dir_path = args["path"]
video1 = args["video1"]
video2 = args["video2"]


cap = cv2.VideoCapture(video1)
cap2 = cv2.VideoCapture(video2)

#Offsets by xframe, frame frames
loffset = start
cap.set(1,loffset);
roffset=start+offset
cap2.set(1,roffset);
if endframe == 0:
    endframe = 5000000

frametext=0
#height,width,layers=frame.shape
#size = (width, height)
outfile1 = video1[:-4] + "_clip_" + str(start) + "_" + str(endframe)+ ".mkv"
outfile2 = video2[:-4] + "_clip_" + str(start) + "_" + str(endframe)+ ".mkv"

fourcc = cv2.VideoWriter_fourcc(*'FFV1')
out = cv2.VideoWriter(outfile1, fourcc, 30, (640,480))
out2 = cv2.VideoWriter(outfile2, fourcc, 30, (640,480))

while(cap.isOpened()):
    frametext=frametext+1
    ret, frame = cap.read()
    ret, frame2 = cap2.read()

    out.write(frame)
    out2.write(frame2)

    if (frametext+loffset) > endframe:
        break

    cv2.imshow('left video',frame)
    cv2.imshow('right video',frame2)

    #move window when first opening
    if frametext == 1:
    	cv2.moveWindow('right video',642, 0)
    	cv2.moveWindow('left video',0, 0)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

out.release()
out2.release()
cap.release()
cap2.release()
cv2.destroyAllWindows()
