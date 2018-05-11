import math
from pulse_data import FramePulseData
from pulse_data import PulseData
from camera import Camera
import sys

#TODO: implement get_z_val()

def depth_map(ostracod_list1, ostracod_list2, framepulsedata, framenum, camera):
    if not isinstance(framepulsedata, FramePulseData):
        sys.exit("fpd must be of type FramePulseData")
    if not isinstance(camera, Camera):
        sys.exit("camera must be of type Camera")
    for o in ostracod_list1:
        if len(o.matches) > 0:
            pd = generate_pulse_data(o, ostracod_list2[o.matches[0][0]], camera)
            framepulsedata.add_pulse_to_frame(framenum, pd)


def generate_pulse_data(ostracod1, ostracod2, camera):
    avg_brightness = (ostracod1.brightness + ostracod2.brightness)/2
    avg_area = (ostracod1.area + ostracod2.area)/2

    z = get_z_val(ostracod1.location[0], ostracod2.location[0], camera.focal_length, camera.baseline)

    real_coordinate_ratio = z/camera.focal_length
    location = [ostracod1.location[0]*real_coordinate_ratio, ostracod2.location[1]*real_coordinate_ratio, z]

    brightness = scale_2d_attribute(avg_brightness, z)
    area = scale_2d_attribute(avg_area, z)
    radius = (area/math.pi)**0.5
    return PulseData(xyz_coord=location, radius=radius, brightness=brightness)


def get_z_val(left_x, right_x, focal_length, baseline):
    return focal_length * baseline / (left_x - right_x)


def scale_2d_attribute(attribute, z_val):
    return attribute*(z_val+1)**2

