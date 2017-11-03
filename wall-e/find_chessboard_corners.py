import cv2
import numpy as np

# This is helpful: 'help(cv2.stereoRectify)' this will give you info on whatever function you want

# Create (x,y,z) object points for all intersections on checkerboard grid
objp = np.zeros((5 * 4, 3), np.float32)
objp[:, :2] = np.mgrid[0:5, 0:4].T.reshape(-1, 2)

# print objp this may need adjustment

# Create empty arrays for oject points and image points from each image
objpoints = []
imgpoints_l = []
imgpoints_r = []

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.1)

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

ret, corners = cv2.findChessboardCorners(img_l,(5,4), cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FILTER_QUADS)
ret_r, corners_r = cv2.findChessboardCorners(img_r,(5,4), cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FILTER_QUADS) # 7,5 works
print ret_r
print ret


# If found, add object points to objpoints array, and add image points (after refining them) to imgpoints array
if ret and ret_r:
    objpoints.append(objp)
    cv2.cornerSubPix(img_l, corners, (5, 5), (-1, -1), criteria)  # refine image points
    cv2.cornerSubPix(img_r, corners_r, (5, 5), (-1, -1), criteria)  # refine image points

    imgpoints_l.append(corners)
    imgpoints_r.append(corners_r)


    # Draw and display the corners
    cv2.drawChessboardCorners(img_l, (5, 4), corners, ret)
    cv2.drawChessboardCorners(img_r, (5, 4), corners, ret)
    cv2.drawChessboardCorners(img_l, (5, 4), corners_r, ret_r)
    cv2.drawChessboardCorners(img_r, (5, 4), corners_r, ret_r)
    cv2.imshow('Image with Corner Points_l', img_l)
    cv2.imshow('Image with Corner Points_r', img_r)
    # cv2.waitKey(0)


# ret_r, mtx_r, dist_r, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints_r, img_r.shape[::-1], None, None)
# ret_l, mtx_l, dist_l, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints_l, img_l.shape[::-1], None, None)
# mtx_l = []
# mtx_r = []
# dst_l = []
# dst_r = []

# im not sure if putting none for the params is ok
ret, mtx_l, dst_l, mtx_r, dst_r, R, T, E, F = cv2.stereoCalibrate(objpoints,imgpoints_l, imgpoints_r,
                                                                  None, None, None, None, img_r.shape[::-1])


print 'shape',img_l.shape
h, w = img_l.shape  # changed image to gray b/c image got error

mtx_l2, roi_l = cv2.getOptimalNewCameraMatrix(mtx_l, dst_l, (w, h), 1, (w, h))
mtx_r2, roi_r = cv2.getOptimalNewCameraMatrix(mtx_r, dst_l, (w, h), 1, (w, h))

# undistort, this appears to do nothing


# stereo rectify
# TODO: Figure out how to use this return values
R1, R2, P1, P2, Q, validPixROI1, validPixROI2 = cv2.stereoRectify(mtx_l, dst_l, mtx_r, dst_r,
                                                                  img_r.shape[::-1], R, T)

new_shape = (1280//2,960//2)
map_l = cv2.initUndistortRectifyMap(mtx_l,dst_l, R1, P1, new_shape, cv2.CV_32F)
map_r = cv2.initUndistortRectifyMap(mtx_r,dst_r, R2, P2, new_shape, cv2.CV_32F)

img_l = cv2.remap(img_l,map_l[0],map_l[1],cv2.INTER_LANCZOS4)
img_r = cv2.remap(img_r,map_r[0],map_r[1],cv2.INTER_LANCZOS4)

cv2.imshow('left und',img_l)
cv2.imshow('right und', img_r)
cv2.waitKey(0)
#
# for line in range(0, img_l.shape / 20)):
#     left_img_remap[line * 20, :] = (0, 0, 255)
#     right_img_remap[line * 20, :] = (0, 0, 255)
#
# cv2.imshow('winname', np.hstack(img_l, img_r))
# cv2.waitKey(0)
# exit(0)

# crop the image
# print roi_l, roi_r
# x,y,w,h = roi
# dst = dst[y:y+h, x:x+w]
#
# os.chdir('Undistorted_frames')
# cv2.imwrite('Undistortionresult.png',dst)
# cv2.imshow('Undistorted Image',dst)
#
