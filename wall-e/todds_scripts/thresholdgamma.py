import numpy as np
import cv2
import argparse
import time

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--path", required=False, default='.', 
        help="path to video frame files default is ./")
ap.add_argument("-f", "--file", required=True, type=str,
	help="file name for video file")
ap.add_argument("-g", "--gamma", required=False, default=0.8,type=float,
	help="value of gamma - a correction for human visualization")
ap.add_argument("-b", "--black", required=False, default=110, type=int,
	help="threshold below which is black. Value ranges from 0-255.")
ap.add_argument("-w", "--white", required=False, default=255, type=int,
	help="threshold above which is white. Values ranges from 0-255")
ap.add_argument("-s", "--start", required=False, default=1, type=int,
	help="frame to start at default = 1")
ap.add_argument("-d", "--delay", required=False, default=0, type=float,
	help="delay time between frames for slo-mo")
ap.add_argument("-v", "--view", required=False, default=1, type=int,
	help="choose whether to view video 1 or not 0")
ap.add_argument("-o", "--outfile", required=False, default="out.mkv", type=str,
	help="Output file default is out.mkv")
args = vars(ap.parse_args())
delay = args["delay"]
gamma = args["gamma"]
black = args["black"]
white = args["white"]
start = args["start"]
view = args["view"]
dir_path = args["path"]
video1 = args["file"]
outfile = args["outfile"]

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
	return cv2.LUT(image, table)

def adjust_gamma(image, gamma=1.0):
	# build a lookup table mapping the pixel values [0, 255] to
	# their adjusted gamma values
	invGamma = 1.0 / gamma
	table = np.array([((i / 255.0) ** invGamma) * 255
		for i in np.arange(0, 256)]).astype("uint8")
	# apply gamma correction using the lookup table
	return cv2.LUT(image, table)



cap = cv2.VideoCapture(video1)
# Define the codec and create VideoWriter object
#frame_width = int(cap.get(3))
#frame_height = int(cap.get(4))
fourcc = cv2.VideoWriter_fourcc(*'FFV1')
out = cv2.VideoWriter(outfile,fourcc, 30, (640,478), False)



#Offsets by xframe, frame frames
loffset = start #called offset because derived from viewing 2 videos which could be offset by x frames
cap.set(1,loffset);

frametext=0
while(cap.isOpened()):
    frametext=frametext+1
    ret, frame = cap.read()
    if not ret:
	break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    clipped = adjust_clip(gray, black=black, white=white)
    gamma = gamma if gamma > 0 else 0.1
    adjusted = adjust_gamma(clipped, gamma=gamma)

#    _, denoised = cv2.threshold(gray, 100, 160, cv2.THRESH_BINARY)
#    _, adjusted = cv2.threshold(gray, black, white, cv2.THRESH_BINARY)

#    adjusted = cv2.fastNlMeansDenoising(denoised,None,10,7,21)

    out.write(adjusted)

    if view == 1:
    	cv2.imshow('frame',adjusted)

    time.sleep(delay)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()
