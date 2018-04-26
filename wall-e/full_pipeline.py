import argparse
from config.keycode_setup import load_keycodes
from stereo_rectification.sr_map_gen import find_and_generate_best_sr_map, SR_MAP_GENERATED_FILENAME
from stereo_rectification.apply_sr import undistort_and_stereo_rectify_videos

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

    # Frame matching process
    # TODO: Using placeholder var's for now. delete this comment and replace with actual logic. Keep the left_offset
    # TODO: right_offset variables, though, it gets used later.
    print("\nStarting the frame matching process.")

    # ~frame matching logic~
    left_offset = 0
    right_offset = 0

    # Stereo Rectification process
    print()
    print("Starting the stereo rectification map generation process.")
    print()
    left_chessboard_video = args.left_video
    right_chessboard_video = args.right_video

    if args.left_cb_video is not None:
        left_chessboard_video = args.left_cb_video
    if args.right_cb_video is not None:
        right_chessboard_video = args.right_cb_video

    find_and_generate_best_sr_map(left_chessboard_video, right_chessboard_video,
                                  left_offset=left_offset, right_offset=right_offset, first_frame=83)

    # Applying Stereo Rectification to video
    print()
    print("Applying the generated stereo rectification map to " + args.left_video + " and " + args.right_video + ".")
    print()
    undistort_and_stereo_rectify_videos(args.left_video, args.right_video, SR_MAP_GENERATED_FILENAME,
                                        left_offset=left_offset, right_offset=right_offset)
