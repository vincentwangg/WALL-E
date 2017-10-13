# Standard imports
import cv2
import numpy as np;

# Read image
im = cv2.imread("Undistortionresult2.png", cv2.IMREAD_GRAYSCALE)
#this makes a negative of the image, and does thresholding. Anything below 110 is 0
retval,imt = cv2.threshold(im, 110, 255, cv2.THRESH_BINARY_INV)

# Setup SimpleBlobDetector parameters.
params = cv2.SimpleBlobDetector_Params()

# Search Parameters
params.minDistBetweenBlobs = 0

params.filterByArea = True
params.minArea = 5
params.filterByCircularity = True
params.minCircularity = 0.4
params.filterByConvexity = True
params.minConvexity = 0.87
#params.filterByInertia = True
#params.minInertiaRatio = 0.1

# Create a detector with the parameters
ver = (cv2.__version__).split('.')
if int(ver[0]) < 3 :
    detector = cv2.SimpleBlobDetector(params)
else :
    detector = cv2.SimpleBlobDetector_create(params)


# Detect blobs.
keypoints = detector.detect(imt)

print len(keypoints)
print keypoints[1].pt[0]
print keypoints[1].pt[1]
print keypoints[1].size

# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# Show keypoints
cv2.imshow("Keypoints", im_with_keypoints)
cv2.waitKey(0)
