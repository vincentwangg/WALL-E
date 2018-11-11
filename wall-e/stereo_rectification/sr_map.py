"""
This module contains everything needed for SR maps. This includes the following:
- A class that holds SR map information
- Functions for writing and reading SR maps to and from a file
"""

import os

import cv2

from definitions import PROJECT_DIR

CAM_MTX_L_LABEL = "cam_mtx_l"
DIST_L_LABEL = "dist_l"
R1_LABEL = "R1"
P1_LABEL = "P1"

CAM_MTX_R_LABEL = "cam_mtx_r"
DIST_R_LABEL = "dist_r"
R2_LABEL = "R2"
P2_LABEL = "P2"

SR_MAP_FILENAME = os.path.join(PROJECT_DIR, "sr_maps/sr_map.yml")


class SrMap:
    """
    Helps with managing SR map information.

    It's highly recommended not to change any of the SR map
    values anytime after initialization.
    """

    def __init__(self, cam_mtx_l, dist_l, R1, P1, cam_mtx_r, dist_r, R2, P2):
        """Constructor for SrMap objects"""

        self.cam_mtx_l = cam_mtx_l
        self.dist_l = dist_l
        self.R1 = R1
        self.P1 = P1

        self.cam_mtx_r = cam_mtx_r
        self.dist_r = dist_r
        self.R2 = R2
        self.P2 = P2

    def generate_maps(self):
        """Generates stereo rectification maps based on the SrMap object values"""

        map_l = cv2.initUndistortRectifyMap(self.cam_mtx_l,
                                            self.dist_l,
                                            self.R1, self.P1,
                                            (640, 478),
                                            cv2.CV_32F)
        map_r = cv2.initUndistortRectifyMap(self.cam_mtx_r,
                                            self.dist_r,
                                            self.R2, self.P2,
                                            (640, 478),
                                            cv2.CV_32F)
        return map_l, map_r

    def write_to_yml_file(self, filename=SR_MAP_FILENAME):
        """Writes the SrMap object to file"""

        sr_map_dict = {CAM_MTX_L_LABEL: self.cam_mtx_l,
                       DIST_L_LABEL: self.dist_l,
                       R1_LABEL: self.R1,
                       P1_LABEL: self.P1,
                       CAM_MTX_R_LABEL: self.cam_mtx_r,
                       DIST_R_LABEL: self.dist_r,
                       R2_LABEL: self.R2,
                       P2_LABEL: self.P2}

        write = 1
        for key in sr_map_dict.keys():
            save_to_yml(filename, key, sr_map_dict[key], w=write)
            write = 0


def get_sr_map_from_yml_file(filename):
    """
    Recreates an SrMap object from file

    :param filename: file path of the file containing the SR map
    :return: Recreated SrMap object
    """

    fs = cv2.FileStorage(filename, cv2.FILE_STORAGE_READ)
    cam_mtx_l = read_from_yml(fs, CAM_MTX_L_LABEL)
    dist_l = read_from_yml(fs, DIST_L_LABEL)
    R1 = read_from_yml(fs, R1_LABEL)
    P1 = read_from_yml(fs, P1_LABEL)

    cam_mtx_r = read_from_yml(fs, CAM_MTX_R_LABEL)
    dist_r = read_from_yml(fs, DIST_R_LABEL)
    R2 = read_from_yml(fs, R2_LABEL)
    P2 = read_from_yml(fs, P2_LABEL)

    return SrMap(cam_mtx_l, dist_l, R1, P1, cam_mtx_r, dist_r, R2, P2)


def generate_maps(filename):
    """Recreates SrMap object from file and generates SR maps in one step."""

    return get_sr_map_from_yml_file(filename).generate_maps()


def save_to_yml(file, name, object, w=0):
    """
    Helper function to write data to a YML file.

    :param file: Filename of file to make changes to
    :param name: Name of data field
    :param object: Value of data field
    :param w: Write mode (0 = append, 1 = truncate write)
    """

    # The first time you write to a file w needs to be 1
    print("Writting to file:", file)
    if w:
        fs = cv2.FileStorage(file, flags=cv2.FILE_STORAGE_WRITE)
    else:
        fs = cv2.FileStorage(file, flags=cv2.FILE_STORAGE_APPEND)
    fs.write(name, object)
    fs.release()


def read_from_yml(fs, name):
    """
    Helper function to read a data field from a YML file.

    :param fs: FileStorage object
    :param name: Name of data field
    :return: Value of data field
    """
    val = fs.getNode(name).mat()
    return val
