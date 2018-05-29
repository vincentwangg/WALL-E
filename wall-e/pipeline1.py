# The script pipeline1.py runs through the following processes:
#   1) Frame matching
#   2) Stereo rectification (SR) map generation
#   3) Applying SR maps to original videos

import argparse

from config.keycode_setup import load_keycodes
from frame_matching.frame_match_intensity import frame_match
from stereo_rectification.apply_sr import undistort_and_stereo_rectify_videos
from stereo_rectification.sr_map_gen import find_and_generate_best_sr_map, SR_MAP_FILENAME
from utils_general.video_frame_player import play_video

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("left_video", help="filename of the left video feed")
    parser.add_argument("right_video", help="filename of the right video feed")
    parser.add_argument("-lc", "--left_cb_video", help="filename of the left video feed's chessboard video (if the "
                                                       "main left video doesn't have a chessboard for stereo "
                                                       "rectification")
    parser.add_argument("-rc", "--right_cb_video", help="filename of the right video feed's chessboard video (if the "
                                                        "main right video doesn't have a chessboard for stereo "
                                                        "rectification")
    args = parser.parse_args()

    load_keycodes()

    print("Welcome to the full WALL-E footage processing experience!!")
    print("This process helps you perform the following in order:")
    print("\t1) Frame matching the videos")
    print("\t2) Finding and generating the best SR map")
    print("\t3) Stereo rectifying the videos")
    print("\nGood luck!")

    print("\nPlease choose your media files.")

    # Frame matching process
    print("\nStarting the frame matching process.")

    # ~frame matching logic~
    # can pass in start and end timstamp if you know where LED flashes occur!
    left_offset, right_offset, _, _ = frame_match(args.left_video, args.right_video, None, None)

    # Show video frame player to verify offset
    left_offset, right_offset = play_video(args.left_video, args.right_video, left_offset, right_offset, 0)

    # Stereo Rectification process
    print("\nStarting the stereo rectification map generation process.\n")
    left_chessboard_video = args.left_video
    right_chessboard_video = args.right_video

    if args.left_cb_video is not None:
        left_chessboard_video = args.left_cb_video
    if args.right_cb_video is not None:
        right_chessboard_video = args.right_cb_video

    find_and_generate_best_sr_map(left_chessboard_video, right_chessboard_video,
                                  left_offset=left_offset, right_offset=right_offset, first_frame=83)

    # Applying Stereo Rectification to video
    print(
        "\nApplying the generated stereo rectification map to " + args.left_video + " and " + args.right_video + ".\n")
    undistort_and_stereo_rectify_videos(args.left_video, args.right_video, SR_MAP_FILENAME,
                                        left_offset=left_offset, right_offset=right_offset)
