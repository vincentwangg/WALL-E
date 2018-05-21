# This pipeline is responsible for matching ostracods between two frames, 3d mapping, and writing
# the blender information to a text file from an FramePulseData object

from utilities.video_frame_loader import VideoFrameLoader
from ostracod_detection.matching import match
from mapping_3d.mapper_3d import depth_map
from mapping_3d.pulse_data import FramePulseData
from mapping_3d.pulse_data import write_frame_pulse_data_to_file
from mapping_3d.camera import Camera
from ostracod_detection.locating import locator
import time
import argparse
from utilities.file_checker import check_if_file_exists

def main():
    parser = argparse.ArgumentParser(description="Reads in left and right videos as well as the camera baseline.")
    parser.add_argument("left_video", help="filename of the left video feed", type=str)
    parser.add_argument("right_video", help="filename of the right video feed", type=str)
    parser.add_argument("baseline", help="The distance between the two stereo cameras", type=float)
    args = parser.parse_args()

    left_file_name = args.left_video
    right_file_name = args.right_video
    baseline = args.baseline

    check_if_file_exists(left_file_name)
    check_if_file_exists(right_file_name)

    vfl = VideoFrameLoader(left_file_name, right_file_name)
    camera = Camera(baseline=baseline, focal_length=100)
    fpd = FramePulseData()

    success_r, right_image = vfl.get_next_right_frame()
    success_l, left_image = vfl.get_next_left_frame()
    frame_num = 0
    locate_time = 0
    match_time = 0
    depth_map_time = 0
    reading_vid_time = 0
    while success_l and success_r:
        print frame_num
        locate_start = time.time()
        ostracod_list_l = locator.get_ostracods(left_image)
        ostracod_list_r = locator.get_ostracods(right_image)
        locate_time += time.time() - locate_start

        match_start = time.time()
        match.match(ostracod_list_l, ostracod_list_r)
        match_time += time.time() - match_start

        depth_map_start = time.time()
        depth_map(ostracod_list_l, ostracod_list_r, framepulsedata=fpd, framenum=frame_num, camera=camera)
        depth_map_time += time.time() - depth_map_start

        vid_start = time.time()
        success_r, right_image = vfl.get_next_right_frame()
        success_l, left_image = vfl.get_next_left_frame()
        reading_vid_time += time.time() - vid_start

        frame_num += 1

    write_start = time.time()
    write_frame_pulse_data_to_file(frame_pulse_data=fpd)
    write_time = time.time() - write_start

    print "depth map time: ", depth_map_time, "seconds"
    print "match time: ", match_time, "seconds"
    print "locating time", locate_time, "seconds"
    print "reading video time", reading_vid_time, "seconds"
    print "write time: ", write_time, "seconds"


if __name__ == '__main__':
    main()
