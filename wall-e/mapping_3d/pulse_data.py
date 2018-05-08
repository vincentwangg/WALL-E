# pulse_data.py contains classes that help store pulse data and write that information to a text file for
# blender_pulse_mapper.py to read.

from numbers import Number

XYZ_COORD_LABEL = "xyz_coord"
RADIUS_LABEL = "radius"
BRIGHTNESS_LABEL = "brightness"

FRAME_PULSE_DATA_FILENAME = "frame_pulse_data.txt"


def verify_xyz_coord_type(xyz_coord):
    if type(xyz_coord) is not list and type(xyz_coord) is not tuple:
        raise TypeError("Coordinates must be a list or tuple.")

    if len(xyz_coord) != 3:
        raise ValueError("Coordinates must have a length of 3.")

    for i in xyz_coord:
        if not isinstance(i, Number):
            raise TypeError("Coordinate values must be a Number type.")


def verify_number_type(value):
    if not isinstance(value, Number):
        raise TypeError("Value must be a Number type.")


class PulseData:
    def __init__(self, xyz_coord, radius, brightness):
        verify_xyz_coord_type(xyz_coord)
        verify_number_type(radius)
        verify_number_type(brightness)

        self.pulse_data = {XYZ_COORD_LABEL: list(xyz_coord), RADIUS_LABEL: radius, BRIGHTNESS_LABEL: brightness}

    def __repr__(self):
        return str(self.pulse_data)


# Helps construct a dictionary with frame # (key) -> list of pulse data (value). Creates a standard for pulse data
# string formatting for blender_pulse_mapper.py to read.
class FramePulseData:
    def __init__(self):
        self.frame_pulse_data = {}

    def add_pulse_to_frame(self, frame_num, *pulse_data_args):
        if frame_num not in self.frame_pulse_data.keys():
            self.frame_pulse_data[frame_num] = []
        for pulse_data in pulse_data_args:
            self.frame_pulse_data[frame_num].append(pulse_data)

    def __repr__(self):
        return str(self.frame_pulse_data)


# pulse_data_by_frame should be a dictionary with frame # (key) -> list of pulse data (value)
def write_pulse_data_to_file(frame_pulse_data, filename=FRAME_PULSE_DATA_FILENAME):
    with open(filename, 'w') as frame_pulse_data_file:
        frame_pulse_data_file.write(str(frame_pulse_data))
