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

map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_32F)

def undistort(img):
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    return undistorted_img


def stereorectify(img_left, img_right):
    # For the 3rd argument, removing those parameters seems to have no effect
    img_left_corners_success, img_left_corner_coords = cv2.findChessboardCorners(img_left, CHECKERBOARD,
                                                                                 cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FILTER_QUADS)
    img_right_corners_success, img_right_corner_coords = cv2.findChessboardCorners(img_right, CHECKERBOARD,
                                                                                   cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FILTER_QUADS)

    # print "Detected corners in left image:\t\t" + str(img_right_corners_success)
    # print "Detected corners in right image:\t" + str(img_left_corners_success)

    if not (img_left_corners_success and img_right_corners_success):
        return False

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

        cv2.drawChessboardCorners(img_left, CHECKERBOARD, img_left_corner_coords, img_left_corners_success)
        cv2.drawChessboardCorners(img_right, CHECKERBOARD, img_right_corner_coords, img_right_corners_success)

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
    # print "Showing left image (stereorectified)"
    cv2.imshow('Right Image - Stereorectified', img_right)
    # print "Showing right image (stereorectified)"

    return True


def main(left_video_filename, right_video_filename):
    # To view the stereo rectification of a single frame, set the start and end frame accordingly (1 frame apart)
    start_frame = 1
    end_frame = 2910
    left_video_offset = 20
    right_video_offset = 0

    frames = []
    print("Starting...")
    for frame_num in range(start_frame, end_frame):
        if frame_num % 20 == 0 or frame_num == 1:
            print("frame_num: " + str(frame_num) + "/" + str(end_frame) + ". Progress: " + str(frame_num * 100 / end_frame) + "%")

        vc_obj_left = cv2.VideoCapture(left_video_filename)
        vc_obj_left.set(cv2.CAP_PROP_POS_FRAMES, frame_num + left_video_offset)
        vc_obj_left_success, img_left = vc_obj_left.read()
        cv2.flip(img_left, -1, img_left)
        convert_to_gray(img_left)

        vc_obj_right = cv2.VideoCapture(right_video_filename)
        vc_obj_right.set(cv2.CAP_PROP_POS_FRAMES, frame_num + right_video_offset)
        vc_obj_right_success, img_right = vc_obj_right.read()
        cv2.flip(img_left, -1, img_right)
        convert_to_gray(img_right)

        img_left_undistorted = undistort(img_left)
        img_right_undistorted = undistort(img_right)

        cv2.imshow('left', img_left)
        cv2.imshow('right', img_right)
        cv2.imshow('left undistorted', img_left_undistorted)
        cv2.imshow('right undistorted', img_right_undistorted)

        if stereorectify(convert_to_gray(img_left_undistorted), convert_to_gray(img_right_undistorted)):
            print("Found frame: " + str(frame_num) + ". Please review the windows and press Y/N to accept/reject frame.")
            key = cv2.waitKey(0)
            yes_key_code = 121
            no_key_code = 110

            if key == no_key_code:
                print("Frame rejected. Current list of working frames: " + str(frames))
            elif key == yes_key_code:
                frames.append(frame_num)
                print("Frame accepted. Current list of working frames: " + str(frames))
            else:
                frames.append(frame_num)
                print("Unknown key. Accepting frame. Current list of working frames: " + str(frames))

    print("The following frames work: ")
    print(frames)

if __name__ == '__main__':
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    else:
        print("Incorrect number of arguments. Usage: ./script left_video_filename right_video_filename")