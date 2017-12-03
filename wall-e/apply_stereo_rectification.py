import cv2
import sys
from stereorectification import undistort
from yaml_utility import read_from_yml

# Undistorts and stereo rectifies videos

# Usage: python apply_stereo_rectification.py left.mkv right.mkv

fourcc = cv2.VideoWriter_fourcc(*'FFV1') ## ffmpeg http://www.fourcc.org/codecs.php

INVERT_RIGHT_VIDEO= 1

# applies map to vc_obj with remap
def apply_rectify_maps(image, map_0, map_1):
    sr_image = cv2.remap(image, map_0, map_1, cv2.INTER_LANCZOS4)
    return sr_image

# returns left map and right map
def generate_maps():
    fs = cv2.FileStorage('sr_maps.yml', cv2.FILE_STORAGE_READ)
    cam_mtx_l = read_from_yml(fs, "cam_mtx_l")
    dist_l = read_from_yml(fs, "dist_l")
    R1 = read_from_yml(fs, "R1")
    P1 = read_from_yml(fs, "P1")

    cam_mtx_r = read_from_yml(fs, "cam_mtx_r")
    dist_r = read_from_yml(fs, "dist_r")
    R2 = read_from_yml(fs, "R2")
    P2 = read_from_yml(fs, "P2")
    map_l = cv2.initUndistortRectifyMap(cam_mtx_l,
                                        dist_l,
                                        R1, P1,
                                        (640,478),
                                        cv2.CV_32F)
    map_r = cv2.initUndistortRectifyMap(cam_mtx_r,
                                        dist_r,
                                        R2, P2,
                                        (640,478),
                                        cv2.CV_32F)
    return (map_l,map_r)

def undistort_and_stereo_rectify_videos(left_filename,right_filename):
    left_vid = cv2.VideoCapture(left_filename)
    right_vid = cv2.VideoCapture(right_filename)

    new_filename_l = left_filename[:-4]+"_stereo_rectified.mkv"
    new_filename_r = right_filename[:-4]+"_stereo_rectified.mkv"

    sr_left_video = cv2.VideoWriter(new_filename_l, fourcc, 30.0, (640,478))
    sr_right_video = cv2.VideoWriter(new_filename_r, fourcc, 30.0, (640,478))

    (l_map,r_map) = generate_maps()

    # Loop over video footage
    print "rectifying footage... this could take a while"
    l_success, l_image = left_vid.read()
    r_success, r_image = right_vid.read()

    while l_success and r_success:
        if INVERT_RIGHT_VIDEO:
            cv2.flip(r_image, -1, r_image)
        undistorted_l_image = undistort(l_image)
        undistorted_r_image = undistort(r_image)
        sr_l_image = apply_rectify_maps(undistorted_l_image, l_map[0], l_map[1]) # apply maps
        sr_r_image = apply_rectify_maps(undistorted_r_image, r_map[0], r_map[1])

        sr_left_video.write(sr_l_image)         # write videos
        sr_right_video.write(sr_r_image)

        l_success, l_image = left_vid.read()    # read next frame
        r_success, r_image = right_vid.read()
    sr_right_video.release()
    sr_left_video.release()
    print "done rectifying! Your videos have the names",new_filename_l,"and", new_filename_r


def main():
    if len(sys.argv) != 3:
        sys.exit("Usage: python apply_stereo_rectification.py left.mkv right.mkv")
    left_filename = str(sys.argv[1])
    right_filename = str(sys.argv[2])
    undistort_and_stereo_rectify_videos(left_filename, right_filename)


if __name__ == '__main__':
    main()