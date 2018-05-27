import cv2
import argparse
from utils_general.video_frame_loader import VideoFrameLoader
from utils_general.file_checker import check_if_file_exists

def crop_left_image(image, crop_val):
    h, w, _ = image.shape
    image = image[0:h - crop_val, :]
    return image

def crop_right_image(image, crop_val):
    h, w, _ = image.shape
    image = image[crop_val:h, :]
    return image


def generate_cropped(left_video_filename, right_video_filename, crop_val):
    fourcc = cv2.VideoWriter_fourcc(*'FFV1')
    vfl = VideoFrameLoader(left_video_filename, right_video_filename)

    new_filename_l = left_video_filename[:-4] + "_cropped.mkv"
    new_filename_r = right_video_filename[:-4] + "_cropped.mkv"

    fc_left_video = cv2.VideoWriter(new_filename_l, fourcc, 30, (640, 478-crop_val))
    fc_right_video = cv2.VideoWriter(new_filename_r, fourcc, 30, (640, 478-crop_val))

    left_succ, left_img = vfl.get_next_left_frame()
    right_succ, right_img = vfl.get_next_right_frame()

    while left_succ and right_succ:
        left_img = crop_left_image(left_img, crop_val)
        right_img = crop_right_image(right_img, crop_val)

        fc_left_video.write(left_img)
        fc_right_video.write(right_img)

        left_succ, left_img = vfl.get_next_left_frame()
        right_succ, right_img = vfl.get_next_right_frame()

    print("Done! Your videos have been placed in the paths \"" +
          new_filename_l + "\" and \"" + new_filename_r + "\"")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("left_video", help="filename of the left video feed")
    parser.add_argument("right_video", help="filename of the right video feed")
    parser.add_argument("crop_value", type=int, help="How many pixels to take off of each frame")

    args = parser.parse_args()

    left_video_filename = args.left_video
    right_video_filename = args.right_video
    crop_val = args.crop_value

    check_if_file_exists(left_video_filename)
    check_if_file_exists(right_video_filename)

    generate_cropped(left_video_filename, right_video_filename, crop_val)


if __name__ == '__main__':
    main()