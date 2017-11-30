import cv2
import os
import sys

def read(fs,name):
    val = fs.getNode(name).type()
    return val

# returns undistorted vc object
def undistort(vc_obj, map1, map2):
    return vc_obj

# applies map to vc_obj with remap
def apply_rectify_maps(vc_obj, l_map, r_map):
    return vc_obj

# writes the corrected vc_obj to a file
def write_to_file(vc_obj,filename):
    return None

def main():
    fs = cv2.FileStorage("sr_maps.yml")
    undistort_map1 = read(fs, "undistort_map1")
    undistort_map2 = read(fs, "undistort_map2")
    l_sr_map_0 = read(fs, "l_sr_map_0")
    l_sr_map_1 = read(fs, "l_sr_map_1")
    r_sr_map_0 = read(fs, "r_sr_map_0")
    r_sr_map_1 = read(fs, "r_sr_map_1")

    # Reads command line arguments to get the videos

    # Turn videos into vc_obj

    # Undistort Videos

    # Apply maps

    # Write the new videos to a file

    return None

if __name__ == '__main__':
    main()