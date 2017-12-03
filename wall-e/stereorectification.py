# Code imported from https://medium.com/@kennethjiang/calibrate-fisheye-lens-using-opencv-part-2-13990f1b157f

import numpy as np
import cv2
from grayscale_converter import convert_to_gray
from yaml_utility import save_to_yml
import sys

# You should replace these 3 lines with the output in calibration step (calibrate.py)
CHECKERBOARD = (8, 6)
DIM=(640, 478) # deinterlaced video is now 640 X 478
K=np.array([[526.756924435422, 0.0, 330.221556181272], [0.0, 478.43311043812145, 249.44524334088075], [0.0, 0.0, 1.0]])
D=np.array([[-0.07527166402108293], [0.006777363197177597], [-0.32231954249568173], [0.43735394851622683]])


def undistort(img):
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_32F) # cv2.CV_16SC2
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    return undistorted_img


def stereorectify(img_left, img_right):
    # For the 3rd argument, removing those parameters seems to have no effect
    img_left_corners_success, img_left_corner_coords = cv2.findChessboardCorners(img_left, CHECKERBOARD,
                                                                                 cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FILTER_QUADS)
    img_right_corners_success, img_right_corner_coords = cv2.findChessboardCorners(img_right, CHECKERBOARD,
                                                                                   cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FILTER_QUADS)

    print "Detected corners in left image:\t\t" + str(img_right_corners_success)
    print "Detected corners in right image:\t" + str(img_left_corners_success)

    # Tuning these parameters does not appear to effect the end result
    max_iterations = 30
    epsilon = 0.0001
    criteria = (cv2.TERM_CRITERIA_MAX_ITER + cv2.TERM_CRITERIA_EPS, max_iterations, epsilon)

    # Create (x,y,z) object points for all intersections on checkerboard grid
    objp = np.zeros((CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)

    # Create empty arrays for object points and image points from each image
    objpoints = []
    img_points_left = []
    img_points_right = []

    # If found, add object points to objpoints array, and add image points (after refining them) to imgpoints array
    if img_left_corners_success and img_right_corners_success:
        objpoints.append(objp)

        # cornerSubPix refines the corner coordinates. (tuning these params does nothing)
        img_points_left = [cv2.cornerSubPix(img_left, img_left_corner_coords, (11, 11), (-1, -1), criteria)]
        img_points_right = [cv2.cornerSubPix(img_right, img_right_corner_coords, (11, 11), (-1, -1), criteria)]

    reprojection_error_left, cam_mtx_l, dist_l, rotation_vec_left, translation_vec_left = cv2.calibrateCamera(
        objpoints,
        img_points_left,
        img_left.shape[::-1],
        None, None)
    reprojection_error_right, cam_mtx_r, dist_r, rotation_vec_right, translation_vec_right = cv2.calibrateCamera(
        objpoints,
        img_points_right,
        img_right.shape[::-1],
        None, None)

    # https://docs.opencv.org/3.1.0/d9/d0c/group__calib3d.html#ga246253dcc6de2e0376c599e7d692303a
    img_left_corners_success, cam_mtx_l, dist_l, cam_mtx_r, dist_r, R, T, E, F = cv2.stereoCalibrate(
        objpoints,
        img_points_left,
        img_points_right,
        cam_mtx_l, dist_l, cam_mtx_r, dist_r,
        img_right.shape[::-1],
        flags= cv2.CALIB_SAME_FOCAL_LENGTH + cv2.CALIB_FIX_FOCAL_LENGTH + cv2.CALIB_ZERO_TANGENT_DIST)
        # cv2.CALIB_USE_INTRINSIC_GUESS

    # stereo rectify
    R1, R2, P1, P2, Q, validPixROI1, validPixROI2 = cv2.stereoRectify(cam_mtx_l,
                                                                      dist_l,
                                                                      cam_mtx_r,
                                                                      dist_r,
                                                                      img_right.shape[::-1],
                                                                      R, T, alpha=0.95)

    map_l = cv2.initUndistortRectifyMap(cam_mtx_l,
                                        dist_l,
                                        R1, P1,
                                        img_left.shape[::-1],
                                        cv2.CV_32F)
    map_r = cv2.initUndistortRectifyMap(cam_mtx_r,
                                        dist_r,
                                        R2, P2,
                                        img_right.shape[::-1],
                                        cv2.CV_32F)

    save_to_yml("sr_maps.yml", "cam_mtx_l", cam_mtx_l, w=1)
    save_to_yml("sr_maps.yml", "dist_l", dist_l)
    save_to_yml("sr_maps.yml", "R1", R1)
    save_to_yml("sr_maps.yml", "P1", P1)

    save_to_yml("sr_maps.yml", "cam_mtx_r", cam_mtx_r)
    save_to_yml("sr_maps.yml", "dist_r", dist_r)
    save_to_yml("sr_maps.yml", "R2", R2)
    save_to_yml("sr_maps.yml", "P2", P2)

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


def main():
    frame_num = 860

    vc_obj_left = cv2.VideoCapture("../Left.mkv")
    vc_obj_left.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
    vc_obj_left_success, img_left = vc_obj_left.read()
    convert_to_gray(img_left)

    vc_obj_right = cv2.VideoCapture("../Right.mkv")
    vc_obj_right.set(cv2.CAP_PROP_POS_FRAMES, frame_num+10)
    vc_obj_right_success, img_right = vc_obj_right.read()
    cv2.flip(img_right, -1, img_right)
    convert_to_gray(img_right)

    img_left_undistorted = undistort(img_left)
    img_right_undistorted = undistort(img_right)

    cv2.imshow('left', img_left)
    cv2.imshow('right', img_right)
    cv2.imshow('left undistorted', img_left_undistorted)
    cv2.imshow('right undistorted', img_right_undistorted)

    stereorectify(convert_to_gray(img_left_undistorted), convert_to_gray(img_right_undistorted))
    cv2.waitKey(0)


if __name__ == '__main__':
    main()