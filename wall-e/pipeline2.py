# This pipeline is responsible for matching ostracods between two frames, 3d mapping, and writing
# the blender information to a text file from an FramePulseData object

import cv2
from utilities.video_frame_loader import VideoFrameLoader
from ostracod_detection.matching.match import match
from mapping_3d.mapper_3d import depth_map
from mapping_3d.pulse_data import FramePulseData
from mapping_3d.pulse_data import write_pulse_data_to_file
from mapping_3d.camera import Camera


if __name__ == '__main__':
    left_file_name = "../videos/45_l.mkv"
    right_file_name = "../videos/45_r.mkv"
    frame_pulse_data_file_name = "test_file.txt"
    baseline = 500
    vfl = VideoFrameLoader(left_file_name, right_file_name)
    # camera = Camera(baseline=baseline)
    fpd = FramePulseData()


    success_r, right_image = vfl.get_next_right_frame()
    success_l, left_image = vfl.get_next_left_frame()
    frame_num = 0

    while success_l and success_r:
        print frame_num
        ostracod_list_l, ostracod_list_r = match(left_image, right_image)
        depth_map(ostracod_list_l, ostracod_list_r, framepulsedata=fpd, framenum=frame_num, camera=camera)
        success_r, right_image = vfl.get_next_right_frame()
        success_l, left_image = vfl.get_next_left_frame()
        frame_num += 1

    write_pulse_data_to_file(frame_pulse_data=fpd)
