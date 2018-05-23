# This pipeline is responsible for matching ostracods between two frames, 3d mapping, and writing
# the blender information to a text file from an FramePulseData object

from utilities.video_frame_loader import VideoFrameLoader
from mapping_3d.mapper_3d import depth_map
from mapping_3d.pulse_data import FramePulseData
from mapping_3d.pulse_data import write_frame_pulse_data_to_file
from mapping_3d.camera import Camera
from ostracod_detection.locating.gen_temporal_ostracods import gen_ostracods
from ostracod_detection.matching.match_temporal import get_ostracod_matches
import time
import argparse
from utilities.file_checker import check_if_file_exists

def main():
    parser = argparse.ArgumentParser(description="Reads in left and right videos as well as the camera baseline.")
    parser.add_argument("left_video", help="filename of the left video feed", type=str)
    parser.add_argument("right_video", help="filename of the right video feed", type=str)
    parser.add_argument("baseline", help="The distance between the two stereo cameras", type=float)
    parser.add_argument("-y", "--yaml_file", default=None, type=str,
                        help="Filename of the yaml file that contains the stereo rectification maps. Default is None")

    args = parser.parse_args()

    left_file_name = args.left_video
    right_file_name = args.right_video
    baseline = args.baseline
    sr_yml_file_name = args.yaml_file

    check_if_file_exists(left_file_name)
    check_if_file_exists(right_file_name)

    ostracod_loc_time = 0
    match_time = 0
    depth_map_time = 0
    reading_vid_time = 0

    ostracod_loc_start = time.time()
    ostracods_l = gen_ostracods(left_file_name)
    ostracods_r = gen_ostracods(right_file_name)
    ostracod_loc_time = time.time() - ostracod_loc_start

    match_start = time.time()
    ostracod_matches = get_ostracod_matches(ostracods_l, ostracods_r)
    match_time = time.time() - match_start

    camera = Camera(baseline=baseline, sr_yml_filename=sr_yml_file_name)
    fpd = FramePulseData()

    depth_map_start = time.time()
    depth_map(ostracod_matches, frame_pulse_data=fpd, camera=camera)
    depth_map_time = time.time() - depth_map_start

    write_start = time.time()
    write_frame_pulse_data_to_file(frame_pulse_data=fpd)
    write_time = time.time() - write_start

    print "ostracod location time: ", ostracod_loc_time, "seconds"
    print "match time: ", match_time, "seconds"
    print "depth map time: ", depth_map_time, "seconds"
    print "write time: ", write_time, "seconds"


if __name__ == '__main__':
    main()
