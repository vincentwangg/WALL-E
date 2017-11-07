import cv2
import numpy as np
import pprint

# This is helpful: 'help(cv2.stereoRectify)' this will give you info on whatever function you want

# Create (x,y,z) object points for all intersections on checkerboard grid
objp = np.zeros((5 * 4, 3), np.float32)
objp[:, :2] = np.mgrid[0:5, 0:4].T.reshape(-1, 2)


# print objp this may need adjustment

# Create empty arrays for oject points and image points from each image
objpoints = []
imgpoints_l = []
imgpoints_r = []


# Tuning these parameters does not appear to effect the end result
criteria = (cv2.TERM_CRITERIA_COUNT + cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.0001)

# deinterlace video with ffmpeg first

# get right image from video
r = cv2.VideoCapture("../Right.ASF")
r.set(1, 710)
succ, img_r = r.read()

# flip image and show both
cv2.flip(img_r,-1,img_r)
img_l = cv2.imread('image.jpg')
cv2.imshow('left',img_l)
cv2.imshow('right',img_r)

# convert to gray scale
img_l = cv2.cvtColor(img_l,cv2.COLOR_BGR2GRAY)
img_r = cv2.cvtColor(img_r,cv2.COLOR_BGR2GRAY)

# cv2.waitKey(0)

# For the 3rd argument, removing those parameters seems to have no effect
ret, corners_l = cv2.findChessboardCorners(img_l,(5,4), cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FILTER_QUADS)
ret_r, corners_r = cv2.findChessboardCorners(img_r,(5,4), cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FILTER_QUADS) # 7,5 works
print ret_r
print ret


# If found, add object points to objpoints array, and add image points (after refining them) to imgpoints array
if ret and ret_r:
    objpoints.append(objp)
    # tuning these params does nothing
    corners_l = cv2.cornerSubPix(img_l, corners_l, (11, 11), (-1, -1), criteria)  # refine image points
    corners_r = cv2.cornerSubPix(img_r, corners_r, (11, 11), (-1, -1), criteria)  # refine image points

    # append image points (think of them as (x,y) in the picture
    imgpoints_l.append(corners_l)
    imgpoints_r.append(corners_r)


    # Draw and display the corners
    # cv2.drawChessboardCorners(img_l, (5, 4), corners_l, ret)
    # cv2.drawChessboardCorners(img_r, (5, 4), corners_l, ret)
    # cv2.drawChessboardCorners(img_l, (5, 4), corners_r, ret_r)
    # cv2.drawChessboardCorners(img_r, (5, 4), corners_r, ret_r)
    # cv2.imshow('Image with Corner Points_l', img_l)
    # cv2.imshow('Image with Corner Points_r', img_r)
    # cv2.waitKey(0)



retval, mtx_l, dst_l, rvecs_l, tvecs_l = cv2.calibrateCamera(objpoints,imgpoints_l,img_l.shape[::-1],None,None)
retval, mtx_r, dst_r, rvecs_r, tvecs_r = cv2.calibrateCamera(objpoints,imgpoints_r,img_r.shape[::-1],None,None)

print rvecs_l,rvecs_r



ret, mtx_l, dst_l, mtx_r, dst_r, R, T, E, F = cv2.stereoCalibrate(objpoints,imgpoints_l,imgpoints_r,
                                                                  mtx_l, dst_l, mtx_r, dst_r, img_r.shape[::-1],
                                                                  flags=cv2.CALIB_FIX_PRINCIPAL_POINT)


h, w = img_l.shape

# mtx_lN, roi_l = cv2.getOptimalNewCameraMatrix(mtx_l, dst_l, (w, h), 1, (w, h))
# mtx_rN, roi_r = cv2.getOptimalNewCameraMatrix(mtx_r, dst_l, (w, h), 1, (w, h))

# undistort, this appears to do nothing


# stereo rectify
# TODO: Figure out how to use this return values
R1, R2, P1, P2, Q, validPixROI1, validPixROI2 = cv2.stereoRectify(mtx_l, dst_l, mtx_r, dst_r,
                                                                  img_r.shape[::-1], R, T, alpha=0.90)

# new_shape = (1280//2,960//2)
map_l = cv2.initUndistortRectifyMap(mtx_l,dst_l, R1, P1, img_r.shape[::-1], cv2.CV_32F)
map_r = cv2.initUndistortRectifyMap(mtx_r,dst_r, R2, P2, img_r.shape[::-1], cv2.CV_32F)


img_l = cv2.remap(img_l,map_l[0],map_l[1],cv2.INTER_LANCZOS4,dst= dst_l)
img_r = cv2.remap(img_r,map_r[0],map_r[1],cv2.INTER_LANCZOS4,dst= dst_r)

for line in range(0, int(img_l.shape[0] / 20)):
    img_l[line * 20, :] = 255
    img_r[line * 20, :] = 255


cv2.imshow('stereo rectified_l',img_l)
cv2.imshow('stereo rectified_r', img_r)
cv2.imwrite('CALIB_FIX_PRINCIPAL_POINT_R.jpg',img_r)
cv2.imwrite('CALIB_FIX_PRINCIPAL_POINT_L.jpg',img_l)


cv2.waitKey(0)
