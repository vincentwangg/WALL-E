import cv2
import numpy as np

# Run help(cv2.functionYouWantToKnowMoreAbout) to find documentation on that function

# todo: deinterlace video with ffmpeg first

# get right image from video
vc_obj_right = cv2.VideoCapture("../Right.ASF")
frame_idx_to_capture = 710
vc_obj_right.set(cv2.CAP_PROP_POS_FRAMES, frame_idx_to_capture)
vc_obj_right_success, img_right = vc_obj_right.read()

# flip image and show both
cv2.flip(img_right, -1, img_right)
img_left = cv2.imread('image.jpg')
cv2.imshow('left', img_left)
cv2.imshow('right', img_right)

# convert to gray scale
img_left = cv2.cvtColor(img_left, cv2.COLOR_BGR2GRAY)
img_right = cv2.cvtColor(img_right, cv2.COLOR_BGR2GRAY)

# For the 3rd argument, removing those parameters seems to have no effect
img_left_corners_success, img_left_corner_coords = cv2.findChessboardCorners(img_left, (5, 4),
                                                                             cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FILTER_QUADS)
img_right_corners_success, img_right_corner_coords = cv2.findChessboardCorners(img_right, (5, 4),
                                                                               cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FILTER_QUADS)  # 7,5 works

print "Detected corners in left image:\t\t" + str(img_right_corners_success)
print "Detected corners in right image:\t" + str(img_left_corners_success)

# Tuning these parameters does not appear to effect the end result
max_iterations = 30
epsilon = 0.0001
criteria = (cv2.TERM_CRITERIA_MAX_ITER + cv2.TERM_CRITERIA_EPS, max_iterations, epsilon)

# Create (x,y,z) object points for all intersections on checkerboard grid
objp = np.zeros((5 * 4, 3), np.float32)
objp[:, :2] = np.mgrid[0:5, 0:4].T.reshape(-1, 2)

# Create empty arrays for object points and image points from each image
objpoints = []
refined_img_points_left = []
refined_img_points_right = []

# If found, add object points to objpoints array, and add image points (after refining them) to imgpoints array
if img_left_corners_success and img_right_corners_success:
    objpoints.append(objp)

    # cornerSubPix refines the corner coordinates. (tuning these params does nothing)
    img_left_corner_coords = cv2.cornerSubPix(img_left, img_left_corner_coords, (11, 11), (-1, -1), criteria)
    img_right_corner_coords = cv2.cornerSubPix(img_right, img_right_corner_coords, (11, 11), (-1, -1), criteria)

    # append image points (think of them as (x,y) in the picture)
    refined_img_points_left.append(img_left_corner_coords)
    refined_img_points_right.append(img_right_corner_coords)

reprojection_error_left, cam_matrix_left, distortion_coeff_left, rotation_vec_left, translation_vec_left = cv2.calibrateCamera(
    objpoints,
    refined_img_points_left,
    img_left.shape[::-1],
    None, None)
reprojection_error_right, cam_matrix_right, distortion_coeff_right, rotation_vec_right, translation_vec_right = cv2.calibrateCamera(
    objpoints,
    refined_img_points_right,
    img_right.shape[::-1],
    None, None)

# https://docs.opencv.org/3.1.0/d9/d0c/group__calib3d.html#ga246253dcc6de2e0376c599e7d692303a
img_left_corners_success, cam_matrix_left, distortion_coeff_left, cam_matrix_right, distortion_coeff_right, R, T, E, F = cv2.stereoCalibrate(
    objpoints,
    refined_img_points_left,
    refined_img_points_right,
    cam_matrix_left, distortion_coeff_left, cam_matrix_right, distortion_coeff_right,
    img_right.shape[::-1],
    flags=cv2.CALIB_FIX_PRINCIPAL_POINT)

h, w = img_left.shape

# stereo rectify
R1, R2, P1, P2, Q, validPixROI1, validPixROI2 = cv2.stereoRectify(cam_matrix_left,
                                                                  distortion_coeff_left,
                                                                  cam_matrix_right,
                                                                  distortion_coeff_right,
                                                                  img_right.shape[::-1],
                                                                  R, T, alpha=0.90)

# new_shape = (1280//2,960//2)
map_l = cv2.initUndistortRectifyMap(cam_matrix_left,
                                    distortion_coeff_left,
                                    R1, P1,
                                    img_right.shape[::-1],
                                    cv2.CV_32F)
map_r = cv2.initUndistortRectifyMap(cam_matrix_right,
                                    distortion_coeff_right,
                                    R2, P2,
                                    img_right.shape[::-1],
                                    cv2.CV_32F)

img_left = cv2.remap(img_left,
                     map_l[0],
                     map_l[1],
                     cv2.INTER_LANCZOS4)
img_right = cv2.remap(img_right,
                      map_r[0],
                      map_r[1],
                      cv2.INTER_LANCZOS4)

for line in range(0, int(img_left.shape[0] / 20)):
    img_left[line * 20, :] = 255
    img_right[line * 20, :] = 255

cv2.imshow('Left Image - Stereorectified', img_left)
print "Showing left image (stereorectified)"
cv2.imshow('Right Image - Stereorectified', img_right)
print "Showing right image (stereorectified)"

cv2.waitKey(0)
