import argparse
from utils_general.file_checker import check_if_file_exists
import cv2
import numpy as np

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("left_video_file_name", help="filename of the left video feed")
    parser.add_argument("right_video_file_name", help="filename of the right video feed")

    args = parser.parse_args()

    if (args_are_correct(args)):
        images = generate_images_with_horizontal_lines(args.left_video_file_name, args.right_video_file_name)
        create_video_from_frame_list(images)
        print "Done!!"


def generate_images_with_horizontal_lines(left_video_file_name, right_video_file_name):
    left_video = cv2.VideoCapture(left_video_file_name)
    right_video = cv2.VideoCapture(right_video_file_name)

    left_image_success, left_image = left_video.read()
    right_image_success, right_image = right_video.read()

    output_images = []
    
    while(left_image_success and right_image_success):
        write_horizontal_lines(left_image)
        write_horizontal_lines(right_image)
        output_images.append(combine_two_frames(left_image, right_image))

        left_image_success, left_image = left_video.read()
        right_image_success, right_image = right_video.read()

    return output_images


def create_video_from_frame_list(image_frame_list):
    if len(image_frame_list) > 0:
        new_file_name = "../videos/testing_sr.mkv"
        fourcc = cv2.VideoWriter_fourcc(*'FFV1')
        fps = 30.0
        width = image_frame_list[0].shape[1]
        height = image_frame_list[0].shape[0]

        test_video = cv2.VideoWriter(new_file_name, fourcc, fps, (width, height))
        for frame in image_frame_list:
            test_video.write(frame)
        print "saved video: " + new_file_name
    else:
        print "image_frame_list was empty"


def combine_two_frames(left_image, right_image):
    left_shape = left_image.shape
    right_shape = right_image.shape

    left_width = left_shape[1]
    left_height = left_shape[0]
    
    right_width = right_shape[1]
    right_height = right_shape[0]

    combined_image = np.zeros([left_height, left_width + right_width, 3], dtype=np.uint8)

    combined_image[:left_height, :left_width, :] = left_image
    combined_image[:left_height, left_width:left_width + right_width, :] = right_image

    return combined_image



def write_horizontal_lines(image):
    for line in range(0, int(image.shape[0] / 20)):
        image[line * 20, :] = 255,255,255


def args_are_correct(args):
    # check_if_file_exits sys.exits if the file does not exist
    check_if_file_exists(args.left_video_file_name)
    check_if_file_exists (args.right_video_file_name)
    return True


if __name__ == '__main__':
    main()