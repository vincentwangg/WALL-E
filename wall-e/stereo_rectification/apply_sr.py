"""
This module provides methods that apply stereo rectification to stereo footage.
"""

import argparse
import os

import cv2

from gui.abstract_screens.utilities.constants import PROGRESS_SCREEN_PERCENT_DONE, PROGRESS_SCREEN_MESSAGE_LIST
from gui.pipeline1.utilities.constants import FRAMES_STEREO_RECTIFIED_PREFIX
from stereo_rectification.sr_map import get_sr_map_from_yml_file
from stereo_rectification.sr_map_gen import undistort, SR_MAP_FILENAME
from utils_general.file_checker import check_if_file_exists
from utils_general.frame_calculations import calculate_video_scan_frame_information
from utils_general.video_frame_loader import VideoFrameLoader

fourcc = cv2.VideoWriter_fourcc(*'FFV1')  # ffmpeg http://www.fourcc.org/codecs.php


# applies map to vc_obj with remap
def apply_rectify_maps(image, map_1, map_2):
    """
    Applies the stereo rectification maps to the specified image.

    Example:
    To stereo rectify an image from the left footage, the following should be run:
        stereo_rectified_left_image = apply_rectify_maps(left_image, left_map[0], left_map[1])

    :param image: OpenCV image to stereo rectify
    :param map_1: Index 0 of SR map
    :param map_2: Index 1 of SR map
    :return: Stereo rectified OpenCV image
    """

    sr_image = cv2.remap(image, map_1, map_2, cv2.INTER_LANCZOS4)
    return sr_image


def undistort_and_stereo_rectify_videos(left_filename, right_filename, yml_filename,
                                        left_offset=0, right_offset=0, show_lines=False):
    """
    Undistorts and stereo rectifies videos by filename and allows for a custom
    YML SR map to be used for stereo rectification.

    :param left_filename: File path of the left video
    :param right_filename: File path of the right video
    :param yml_filename: File path of the YML SR map to be used
    :param left_offset: Frame offset of the left video
    :param right_offset: Frame offset of the right video
    :param show_lines: Whether or not the final video should have horizontal white lines to indicate SR results
    """

    video_frame_loader = VideoFrameLoader(left_filename, right_filename)

    new_filename_l = left_filename[:-4] + "_stereo_rectified.mkv"
    new_filename_r = right_filename[:-4] + "_stereo_rectified.mkv"

    sr_left_video = cv2.VideoWriter(new_filename_l, fourcc, 30, (640, 478))
    sr_right_video = cv2.VideoWriter(new_filename_r, fourcc, 30, (640, 478))

    l_map, r_map = get_sr_map_from_yml_file(yml_filename).generate_maps()

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


# Logic behind Apply Sr GUI screen
def apply_sr_gui_logic(controller):
    """
    Does the same thing as undistort_and_stereo_rectify_videos(),
    except the functionality is suited for the GUI's backend logic.

    Compared to the original function, this one doesn't output
    to console and updates the GUI regularly through the controller.

    :param controller: The GUI controller for pipeline 1
    """

    first_frame = controller.apply_sr_frame_range.first_frame
    last_frame_inclusive = controller.apply_sr_frame_range.last_frame_inclusive
    left_offset = controller.video_offsets.left_offset
    right_offset = controller.video_offsets.right_offset
    video_frame_loader = controller.video_frame_loader
    left_filename = video_frame_loader.left_feed_filename
    right_filename = video_frame_loader.right_feed_filename

    new_filename_l = left_filename[:-4] + "_stereo_rectified.mkv"
    new_filename_r = right_filename[:-4] + "_stereo_rectified.mkv"

    sr_left_video = cv2.VideoWriter(new_filename_l, fourcc, 30, (640, 478))
    sr_right_video = cv2.VideoWriter(new_filename_r, fourcc, 30, (640, 478))

    l_map, r_map = controller.sr_map.generate_maps()

    first_frame_left, last_frame_left, first_frame_right, last_frame_right, num_frames_to_scan = \
        calculate_video_scan_frame_information(first_frame,
                                               last_frame_inclusive,
                                               left_offset,
                                               right_offset,
                                               video_frame_loader)

    video_frame_loader.set_left_current_frame_num(first_frame_left)
    video_frame_loader.set_right_current_frame_num(first_frame_right)

    num_frames_processed = 0

    update_apply_sr_ui(controller, num_frames_processed, num_frames_to_scan)

    while True:
        left_frame_num = video_frame_loader.get_left_current_frame_num()
        right_frame_num = video_frame_loader.get_right_current_frame_num()

        # If one of the videos reach their last frame to scan
        if left_frame_num > last_frame_left or right_frame_num > last_frame_right:
            break

        l_success, left_img = video_frame_loader.get_next_left_frame()
        r_success, right_img = video_frame_loader.get_next_right_frame()

        # If one of the videos reach the end of video
        if not l_success or not r_success:
            break

        sr_l_image = apply_rectify_maps(undistort(left_img), l_map[0], l_map[1])
        sr_r_image = apply_rectify_maps(undistort(right_img), r_map[0], r_map[1])

        sr_left_video.write(sr_l_image)
        sr_right_video.write(sr_r_image)

        num_frames_processed += 1

        if num_frames_processed % 10 == 0:
            update_apply_sr_ui(controller, num_frames_processed, num_frames_to_scan)

    sr_left_video.release()
    sr_right_video.release()

    # Set output video file paths
    controller.left_video_filename_sr = os.path.abspath(new_filename_l)
    controller.right_video_filename_sr = os.path.abspath(new_filename_r)

    update_apply_sr_ui(controller, num_frames_processed, num_frames_to_scan)


def update_apply_sr_ui(controller, frames_processed, total_frames):
    """Updates the UI progress screen"""

    progress_percent = frames_processed * 100.0 / total_frames
    frames_processed_message = create_frames_stereo_rectified_text(frames_processed, total_frames, progress_percent)
    controller.update_frame({
        PROGRESS_SCREEN_PERCENT_DONE: progress_percent,
        PROGRESS_SCREEN_MESSAGE_LIST: [
            frames_processed_message
        ]
    })


def create_frames_stereo_rectified_text(frames_processed, total_frames, progress_percent):
    """
    Creates a string that shows how many frames have been stereo rectified.

    :param frames_processed: Number of frames that have been stereo rectified
    :param total_frames: Total number of frames to process
    :param progress_percent: Percentage of frames that have been processed
    :return:
    """

    return FRAMES_STEREO_RECTIFIED_PREFIX + str(frames_processed) + "/" + str(total_frames) + \
           " (" + str(round(progress_percent, 2)) + "%)"


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("left_video", help="filename of the left video feed")
    parser.add_argument("right_video", help="filename of the right video feed")
    parser.add_argument("-y", "--yaml_file", default=SR_MAP_FILENAME,
                        help="filename of the yaml file that contains the stereo rectification maps. default is a "
                             "file named \"" + SR_MAP_FILENAME + "\" in the same directory as this script.")
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
