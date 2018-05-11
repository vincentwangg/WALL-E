# Use this script to play a video frame by frame.
#
# How to use:
# 1) Start the script
# 2) Put the windows that pop up into focus.
# 3) Use the arrow keys to navigate the video. The following buttons do certain actions:
#      Left arrow key       : Go back a frame
#      Right arrow key      : Go forward a frame
#      Up arrow key         : Go forward 30 frames
#      Down arrow key       : Go backwards 30 frames
#      A key                : Increase left offset by 5
#      S key                : Increase left offset by 1
#      D key                : Increase right offset by 1
#      F key                : Increase right offset by 5
#      Q key                : Quit the frame player

import argparse
from config.keycode_setup import *
from utilities.video_frame_loader import VideoFrameLoader

frame_actions = {}
left_offset_actions = {}
right_offset_actions = {}


def normalize_offsets(left_offset, right_offset):
    smaller_offset = min([left_offset, right_offset])
    return (left_offset - smaller_offset), (right_offset - smaller_offset)


def play_video(left_video_filename, right_video_filename, left_offset=0, right_offset=0, first_frame=0):
    init_keycode_actions()

    original_left_offset = left_offset
    original_right_offset = right_offset

    frame_loader = VideoFrameLoader(left_video_filename, right_video_filename)

    frame_num = first_frame
    while True:
        left_frame_num = frame_num + left_offset
        right_frame_num = frame_num + right_offset

        vc_obj_left_success, img_left = frame_loader.get_left_frame(left_frame_num)
        vc_obj_right_success, img_right = frame_loader.get_right_frame(right_frame_num)

        if not vc_obj_left_success or not vc_obj_right_success:
            print("Video has ended.")
            break

        left_image_title = "Left Feed: Frame " + str(left_frame_num)
        right_image_title = "Right Feed: Frame " + str(right_frame_num)

        cv2.imshow(left_image_title, img_left)
        cv2.imshow(right_image_title, img_right)

        cv2.moveWindow(left_image_title, 0, 0)
        cv2.moveWindow(right_image_title, img_left.shape[1], 0)

        print("\nControls: ")
        print("\tLeft/Right : Go back/forward a frame")
        print("\tUp/Down    : Go forward/backward 30 frames")
        print("\tA or S     : Increase left offset by 5 or 1")
        print("\tD or F     : Increase right offset by 1 or 5")
        print("\tY          : Display and keep left/right offsets")
        print("\tQ          : Quit the frame player (Make no changes to left/right offsets)")

        keycode = cv2.waitKey(0)
        cv2.destroyAllWindows()

        if keycode in frame_actions.keys():
            frame_num = frame_num + frame_actions[keycode]
        elif keycode in left_offset_actions.keys():
            left_offset = left_offset + left_offset_actions[keycode]
        elif keycode in right_offset_actions.keys():
            right_offset = right_offset + right_offset_actions[keycode]
        elif keycode == get_keycode_from_key_code_entry(Y_KEY):
            print("\nNew offsets:")
            left_offset, right_offset = normalize_offsets(left_offset, right_offset)
            print_offsets(left_offset, right_offset)
            return left_offset, right_offset
        elif keycode == get_keycode_from_key_code_entry(Q_KEY):
            print("\nNo changes made to left/right offsets.")
            print_offsets(original_left_offset, original_right_offset)
            return original_left_offset, original_right_offset

        if frame_num < 0:
            frame_num = 0


def print_offsets(left_offset, right_offset):
    print("\tLeft offset  : " + str(left_offset))
    print("\tRight offset : " + str(right_offset))


def init_keycode_actions():
    load_keycodes()
    frame_actions[get_keycode_from_key_code_entry(LEFT_ARROW_KEY)] = -1
    frame_actions[get_keycode_from_key_code_entry(RIGHT_ARROW_KEY)] = 1
    frame_actions[get_keycode_from_key_code_entry(UP_ARROW_KEY)] = 30
    frame_actions[get_keycode_from_key_code_entry(DOWN_ARROW_KEY)] = -30
    left_offset_actions[get_keycode_from_key_code_entry(A_KEY)] = 5
    left_offset_actions[get_keycode_from_key_code_entry(S_KEY)] = 1
    right_offset_actions[get_keycode_from_key_code_entry(D_KEY)] = 1
    right_offset_actions[get_keycode_from_key_code_entry(F_KEY)] = 5


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("left_video", help="filename of the left video feed")
    parser.add_argument("right_video", help="filename of the right video feed")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-l", "--left_offset", type=int, default=0,
                       help="offset of left video feed. left feed will start the specified amount of frames"
                            " earlier than normal")
    group.add_argument("-r", "--right_offset", type=int, default=0,
                       help="offset of right video feed. right feed will start the "
                            "specified amount of frames earlier than normal")
    parser.add_argument("-f", "--first_frame", type=int, default=0,
                        help="frame to start the videos on")
    args = parser.parse_args()

    if args.first_frame < 0:
        sys.exit("First frame must be greater than or equal to 0.")
    if args.left_offset < 0:
        sys.exit("Left offset must be greater than or equal to 0.")
    if args.right_offset < 0:
        sys.exit("Right offset must be greater than or equal to 0.")

    play_video(args.left_video, args.right_video, args.left_offset, args.right_offset, args.first_frame)
