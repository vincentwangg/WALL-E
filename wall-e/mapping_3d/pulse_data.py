"""
Contains classes that help store pulse information.
"""

import ast
import os
from numbers import Number

from definitions import MAPPING_3D_DIR

XYZ_COORD_LABEL = "c"
RADIUS_LABEL = "r"
BRIGHTNESS_LABEL = "b"

Z_COORD_IDX = 2

FRAME_PULSE_DATA_FILENAME = os.path.join(MAPPING_3D_DIR, "frame_pulse_data.txt")


def verify_xyz_coord_type(xyz_coord):
    """
    Input checker function that makes sure the value for coordinates is valid.

    XYZ coordinates have to be a list or tuple of length 3, containing numbers and a Z coordinate of at least 0.

    :param xyz_coord: Coordinate location of a pulse
    """

    if type(xyz_coord) is not list and type(xyz_coord) is not tuple:
        raise TypeError("Coordinates must be a list or tuple.")

    if len(xyz_coord) != 3:
        raise ValueError("Coordinates must have a length of 3.")

    for i in xyz_coord:
        check_value_is_number_type(i)

    if xyz_coord[Z_COORD_IDX] <= 0:
        raise ValueError("Z-coordinate has to be greater than 0. Value causing error: " + str(xyz_coord[Z_COORD_IDX]))


def verify_radius_value(radius):
    """
    Input checker function that makes sure the value for radius is valid.

    Radius has to be a number with a value at least 0.

    :param xyz_coord: Radius of a pulse
    """

    check_value_is_number_type(radius)

    if radius <= 0:
        raise ValueError("Radius must be greater than 0. Value causing error: " + str(radius))


def verify_brightness_value(brightness):
    """
    Input checker function that makes sure the value for brightness is valid.

    Brightness has to be a number in the range [0, 1].

    :param xyz_coord: Coordinate location of a pulse
    """

    check_value_is_number_type(brightness)

    if brightness < 0 or brightness > 1:
        raise ValueError("Brightness value must be within range [0, 1]. Value causing error: " + str(brightness))


def check_value_is_number_type(value):
    """
    Checks if a value is a number type.

    :param value: Value that should be a number type
    """
    if not isinstance(value, Number):
        raise TypeError("Value must be a Number type.")


class PulseData:
    """
    Holds information about a pulse.

    That information is the coordinate, radius, and brightness of a pulse.
    """

    def __init__(self, xyz_coord, radius, brightness):
        """
        Constructor

        Takes values for the details of a pulse and makes sure those values are valid.
        """
        verify_xyz_coord_type(xyz_coord)
        verify_radius_value(radius)
        verify_brightness_value(brightness)

        self.xyz_coord = list(xyz_coord)
        self.radius = radius
        self.brightness = brightness

        self.pulse_data = {XYZ_COORD_LABEL: self.xyz_coord,
                           RADIUS_LABEL: self.radius,
                           BRIGHTNESS_LABEL: self.brightness}

    def __repr__(self):
        return str(self.pulse_data)


#
class FramePulseData:
    """
    Helps construct a dictionary with frame # (key) -> list of pulse data (value).

    Creates a standard for pulse data string formatting for blender_pulse_mapper.py to read.
    """

    def __init__(self):
        """Constructor"""
        self.frame_pulse_data = {}

    def __repr__(self):
        return str(self.frame_pulse_data)

    def add_pulse_to_frame(self, frame_num, *pulse_data_args):
        """Adds a pulse data object to the specified frame number."""

        for pulse_data in pulse_data_args:
            if pulse_data is not None:
                if frame_num not in self.frame_pulse_data.keys():
                    self.frame_pulse_data[frame_num] = []
                self.frame_pulse_data[frame_num].append(pulse_data)


def write_frame_pulse_data_to_file(frame_pulse_data, filename=FRAME_PULSE_DATA_FILENAME):
    """
    Writes the frame pulse data to file

    pulse_data_by_frame should be a dictionary with frame # (key) -> list of pulse data (value)
    Format for writing to file

    Example:
        {3: [list of pulses]}
        {5: [list of pulses]} and so on
    """

    with open(filename, 'w') as frame_pulse_data_file:
        for frame_num in frame_pulse_data.frame_pulse_data.keys():
            frame_pulse_data_file.write(str({frame_num: frame_pulse_data.frame_pulse_data[frame_num]}) + "\n")


def read_frame_pulse_data_from_file(filename=FRAME_PULSE_DATA_FILENAME):
    """
    Reads and recreates a frame pulse data object from the specified file.

    :param filename: File with the frame pulse data information
    :return: Recreated frame pulse data object
    """
    with open(filename, 'r') as fpd_file:
        fpd_list = fpd_file.readlines()

        fpd = FramePulseData()
        for data in fpd_list:
            fpd_dict = ast.literal_eval(data)
            for frame_num in fpd_dict.keys():
                pulse_list = fpd_dict[frame_num]
                for pulse in pulse_list:
                    fpd.add_pulse_to_frame(frame_num, PulseData(pulse[XYZ_COORD_LABEL],
                                                                pulse[RADIUS_LABEL],
                                                                pulse[BRIGHTNESS_LABEL]))

        return fpd
