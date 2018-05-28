# This pipeline is responsible for matching ostracods between two frames, 3d mapping, and writing
# the blender information to a text file from an FramePulseData object

from stereo_rectification.sr_map_gen import undistort
from ostracod_detection.matching import match
from mapping_3d.mapper_3d import depth_map_frame
from mapping_3d.pulse_data import FramePulseData
from mapping_3d.pulse_data import write_frame_pulse_data_to_file
from mapping_3d.camera import Camera
from ostracod_detection.locating import locator
from utilities.video_cropper import crop_right_image
from utilities.video_cropper import crop_left_image
from utils_general.file_checker import check_if_file_exists
from utils_general.video_frame_loader import VideoFrameLoader
import cv2
import random
import blender_script


def component():
  return random.randint(0, 255)


def random_color():
    return component(), component(), component()


def draw_circle(image, coordinates, color):
    loc = (coordinates[0], coordinates[1])
    cv2.circle(image, loc, 8, color, thickness=3, lineType=8, shift=0)


def draw_ostracods(image, ostracods):
    image_c = image.copy()
    for o in ostracods:
        color = (255, 0, 0)
        draw_circle(image_c, o.location, color)
    return image_c


def draw_matches(l_list, r_list, image_l, image_r):
    image_l = image_l.copy()
    image_r = image_r.copy()
    for o in l_list:
        if len(o.matches) > 0:
            color = random_color()
            draw_circle(image_l, o.location, color)
            for m in o.matches:
                draw_circle(image_r, r_list[m[0]].location, color)
    return image_l, image_r


def main():
    left_file_name = '../videos/EGD_left.mkv'
    right_file_name = '../videos/EGD_right.mkv'

    FRAME_NUM = 40890
    OFFSET = 10

    baseline = 400
    focal_length = 530

    check_if_file_exists(left_file_name)
    check_if_file_exists(right_file_name)

    vfl = VideoFrameLoader(left_file_name, right_file_name)
    camera = Camera(baseline=baseline, focal_length=focal_length)
    fpd = FramePulseData()

    # original images
    success_r, right_image = vfl.get_right_frame(FRAME_NUM)
    success_l, left_image = vfl.get_left_frame(FRAME_NUM)
    right_image = cv2.flip(right_image, -1)

    cv2.imshow("right_image_step_1", right_image)
    cv2.imshow("left_image_step_1", left_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # frame matching
    success_r, right_image = vfl.get_right_frame(FRAME_NUM + OFFSET)
    success_l, left_image = vfl.get_left_frame(FRAME_NUM)
    right_image = cv2.flip(right_image, -1)

    cv2.imshow("right_image_frame_matched", right_image)
    cv2.imshow("left_image_frame_matched", left_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # correct for fisheye
    right_image = undistort(right_image)
    left_image = undistort(left_image)

    cv2.imshow("right_correct_for_fisheye", right_image)
    cv2.imshow("left_correct_for_fisheye", left_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Stereo Rectification
    right_image = crop_right_image(right_image, 40)
    left_image = crop_left_image(left_image, 40)

    cv2.imshow("right_image_stereo_rectified", right_image)
    cv2.imshow("left_image_stereo_rectified", left_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Locate ostracods
    ostracod_list_l = locator.get_ostracods(left_image)
    ostracod_list_r = locator.get_ostracods(right_image)

    left_located = draw_ostracods(left_image, ostracod_list_l)
    right_located = draw_ostracods(right_image, ostracod_list_r)

    cv2.imshow("right_image_located", right_located)
    cv2.imshow("left_image_located", left_located)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Match ostracods
    match.match(ostracod_list_l, ostracod_list_r, threshold=10)
    images = draw_matches(ostracod_list_l, ostracod_list_r, left_image, right_image)

    cv2.imshow("right_image_matched", images[1])
    cv2.imshow("left_image_matched", images[0])
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # 3D mapping
    depth_map_frame(ostracod_list_l, ostracod_list_r, framepulsedata=fpd, framenum=0, camera=camera)
    write_frame_pulse_data_to_file(frame_pulse_data=fpd)
    blender_script.main()


if __name__ == '__main__':
    main()
