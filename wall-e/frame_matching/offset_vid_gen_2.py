import cv2
import argparse
from utilities.video_frame_loader import VideoFrameLoader
from utilities.file_checker import check_if_file_exists
import sys


def generate_corrected(left_video_filename, right_video_filename, left_offset, right_offset):
    fourcc = cv2.VideoWriter_fourcc(*'FFV1')
    vfl = VideoFrameLoader(left_video_filename, right_video_filename)

    new_filename_l = left_video_filename[:-4] + "_frame_corrected.mkv"
    new_filename_r = right_video_filename[:-4] + "_frame_corrected.mkv"

    fc_left_video = cv2.VideoWriter(new_filename_l, fourcc, 30, (640, 478))
    fc_right_video = cv2.VideoWriter(new_filename_r, fourcc, 30, (640, 478))

    left_succ, left_img = vfl.get_left_frame(left_offset)
    right_succ, right_img = vfl.get_right_frame(right_offset)

    while(left_succ and right_succ):
        fc_left_video.write(left_img)
        fc_right_video.write(right_img)

        left_succ, left_img = vfl.get_next_left_frame()
        right_succ, right_img = vfl.get_next_right_frame()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("left_video", help="filename of the left video feed")
    parser.add_argument("right_video", help="filename of the right video feed")

    parser.add_argument("-l", "--left_offset", type=int, default=0,
                       help="offset of left video feed. left feed will start the specified amount of frames"
                            " earlier than normal")
    parser.add_argument("-r", "--right_offset", type=int, default=0,
                       help="offset of right video feed. right feed will start the "
                            "specified amount of frames earlier than normal")

    args = parser.parse_args()

    left_video_filename = args.left_video
    right_video_filename = args.right_video
    left_offset = args.left_offset
    right_offset = args.right_offset

    if left_offset < 0 or right_offset < 0:
        sys.exit("Error: offsets must be greater or equal to zero")

    check_if_file_exists(left_video_filename)
    check_if_file_exists(right_video_filename)

    generate_corrected(left_video_filename, right_video_filename, left_offset, right_offset)


if __name__ == '__main__':
    main()