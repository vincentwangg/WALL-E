# pulse_data.py contains a class that holds information about pulse location, radius, and brightness.

from numbers import Number


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

        self.xyz_coord = list(xyz_coord)
        self.radius = radius
        self.brightness = brightness
