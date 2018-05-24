import cv2
import argparse
from utilities.video_frame_loader import VideoFrameLoader
from utilities.file_checker import check_if_file_exists

def crop_left_image(image):
    h, w, _ = image.shape
    image = image[0:h - 45, :]
    return image

def crop_right_image(image):
    h, w, _ = image.shape
    image = image[45:h, :]
    return image


def generate_cropped(left_video_filename, right_video_filename):
    fourcc = cv2.VideoWriter_fourcc(*'FFV1')
    vfl = VideoFrameLoader(left_video_filename, right_video_filename)

    new_filename_l = left_video_filename[:-4] + "_cropped.mkv"
    new_filename_r = right_video_filename[:-4] + "_cropped.mkv"

    fc_left_video = cv2.VideoWriter(new_filename_l, fourcc, 30, (640, 478))
    fc_right_video = cv2.VideoWriter(new_filename_r, fourcc, 30, (640, 478))

    left_succ, left_img = vfl.get_next_left_frame()
    right_succ, right_img = vfl.get_next_right_frame()

    while left_succ and right_succ:
        left_img = crop_left_image(left_img)
        right_img = crop_right_image(right_img)

        fc_left_video.write(left_img)
        fc_right_video.write(right_img)

        left_succ, left_img = vfl.get_next_left_frame()
        right_succ, right_img = vfl.get_next_right_frame()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("left_video", help="filename of the left video feed")
    parser.add_argument("right_video", help="filename of the right video feed")

    args = parser.parse_args()

    left_video_filename = args.left_video
    right_video_filename = args.right_video

    check_if_file_exists(left_video_filename)
    check_if_file_exists(right_video_filename)

    generate_cropped(left_video_filename, right_video_filename)


if __name__ == '__main__':
    main()