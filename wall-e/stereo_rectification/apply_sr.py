# Before running this, convert the videos to mkv using handbrake
# Undistorts and stereo rectifies videos 2:53,

import argparse
import cv2
import os
from stereo_rectification.sr_map_gen import undistort, SR_MAP_GENERATED_FILENAME
from utilities.file_checker import check_if_file_exists
from utilities.yaml_utility import read_from_yml
from utilities.video_frame_loader import VideoFrameLoader

fourcc = cv2.VideoWriter_fourcc(*'FFV1')  # ffmpeg http://www.fourcc.org/codecs.php


# applies map to vc_obj with remap
def apply_rectify_maps(image, map_0, map_1):
    sr_image = cv2.remap(image, map_0, map_1, cv2.INTER_LANCZOS4)
    return sr_image


# returns left map and right map
def generate_maps(yml_filename):
    fs = cv2.FileStorage(yml_filename, cv2.FILE_STORAGE_READ)
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
                                        (640, 478),
                                        cv2.CV_32F)
    map_r = cv2.initUndistortRectifyMap(cam_mtx_r,
                                        dist_r,
                                        R2, P2,
                                        (640, 478),
                                        cv2.CV_32F)
    return map_l, map_r


def undistort_and_stereo_rectify_videos(left_filename, right_filename, yml_filename,
                                        left_offset=0, right_offset=0, show_lines=False):
    video_frame_loader = VideoFrameLoader(left_filename, right_filename)

    new_filename_l = left_filename[:-4] + "_stereo_rectified.mkv"
    new_filename_r = right_filename[:-4] + "_stereo_rectified.mkv"

    sr_left_video = cv2.VideoWriter(new_filename_l, fourcc, 30, (640, 478))
    sr_right_video = cv2.VideoWriter(new_filename_r, fourcc, 30, (640, 478))

    (l_map, r_map) = generate_maps(yml_filename)

    # Loop over video footage
    print("Rectifying footage.... This could take a while.")

    frame = 0

    l_success, l_image = video_frame_loader.get_left_frame(frame + left_offset)
    r_success, r_image = video_frame_loader.get_right_frame(frame + right_offset)

    while l_success and r_success:

        if frame % 30 is 0:
            print(str(frame) + " frames rectified. " + str(frame / 30) + " seconds of footage written to file.")

        undistorted_l_image = undistort(l_image)
        undistorted_r_image = undistort(r_image)
        sr_l_image = apply_rectify_maps(undistorted_l_image, l_map[0], l_map[1])  # apply maps
        sr_r_image = apply_rectify_maps(undistorted_r_image, r_map[0], r_map[1])

        # Draw white lines to show how results of stereo rectification in video
        if show_lines:
            for line in range(0, int(sr_l_image.shape[0] / 20)):
                sr_l_image[line * 20, :] = 255
                sr_r_image[line * 20, :] = 255

        sr_left_video.write(sr_l_image)  # write videos
        sr_right_video.write(sr_r_image)

        frame = frame + 1
        l_success, l_image = video_frame_loader.get_next_left_frame()
        r_success, r_image = video_frame_loader.get_next_right_frame()

    sr_left_video.release()
    sr_right_video.release()

    full_filename_l = os.path.abspath(new_filename_l)
    full_filename_r = os.path.abspath(new_filename_r)
    print("Done rectifying! Your videos have been placed in the paths \"" +
          full_filename_l + "\" and \"" + full_filename_r + "\"")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("left_video", help="filename of the left video feed")
    parser.add_argument("right_video", help="filename of the right video feed")
    parser.add_argument("-y", "--yaml_file", default=SR_MAP_GENERATED_FILENAME,
                        help="filename of the yaml file that contains the stereo rectification maps. default is a "
                             "file named \"" + SR_MAP_GENERATED_FILENAME + "\" in the same directory as this script.")
    parser.add_argument("-w", "--show_lines", type=bool, default=False,
                        help="True if white lines to help show results of stereo rectification are wanted. False if not")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-l", "--left_offset", type=int, default=0,
                       help="offset of left video feed. left feed will start the specified amount of frames"
                            " earlier than normal")
    group.add_argument("-r", "--right_offset", type=int, default=0,
                       help="offset of right video feed. right feed will start the "
                            "specified amount of frames earlier than normal")

    args = parser.parse_args()

    left_video_filename = args.left_video
    right_video_filename = args.right_video

    check_if_file_exists(left_video_filename)
    check_if_file_exists(right_video_filename)

    undistort_and_stereo_rectify_videos(left_video_filename, right_video_filename, args.yaml_file,
                                        left_offset=args.left_offset, right_offset=args.right_offset,
                                        show_lines=args.show_lines)
