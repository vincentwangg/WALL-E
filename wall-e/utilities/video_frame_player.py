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
#      Z key                : Your classic ctrl-Z
#      Other keys           : Go forward a frame

import argparse
from config.keycode_setup import *
from utilities.video_frame_loader import VideoFrameLoader

frame_actions = {}


def play_video(left_video_filename, right_video_filename, left_offset=0, right_offset=0, first_frame=0):
    frame_loader = VideoFrameLoader(left_video_filename, right_video_filename)

    frame_num = first_frame
    frame_history = []
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

        frame_history.append(frame_num)
        print(frame_history)
        keycode = cv2.waitKey(0)
        cv2.destroyAllWindows()

        if keycode == get_keycode_from_key_code_entry(Z_KEY):
            print("hey")
            print(frame_history)
            if len(frame_history) > 1:
                frame_history.pop()
                frame_num = frame_history.pop()
            else:
                frame_num = 0
                frame_history = [0]
            print(frame_history)
        elif keycode in frame_actions.keys():
            frame_num = frame_num + frame_actions[keycode]
        else:
            frame_num = frame_num + 1

        if frame_num < 0:
            frame_num = 0


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

    load_keycodes()
    frame_actions[get_keycode_from_key_code_entry(LEFT_ARROW_KEY)] = -1
    frame_actions[get_keycode_from_key_code_entry(RIGHT_ARROW_KEY)] = 1
    frame_actions[get_keycode_from_key_code_entry(UP_ARROW_KEY)] = 30
    frame_actions[get_keycode_from_key_code_entry(DOWN_ARROW_KEY)] = -30

    play_video(args.left_video, args.right_video, args.left_offset, args.right_offset, args.first_frame)
