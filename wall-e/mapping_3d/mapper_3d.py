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
    avg_brightness = (ostracod1.brightness + ostracod2.brightness) / 2
    avg_area = (ostracod1.area + ostracod2.area) / 2

    location = get_coord(ostracod1.location, ostracod2.location, camera.focal_length, camera.baseline)
    z = location[2]

    brightness = scale_2d_attribute(avg_brightness, z)
    area = scale_2d_attribute(avg_area, z)
    radius = (area/math.pi)**0.5
    return PulseData(xyz_coord=location, radius=radius, brightness=brightness)


def get_coord(left_coord, right_coord, focal_length, baseline):
    # hardcode pixel widths
    pixel_width = 0.0084 #mm
    pixel_height = 0.0098 #mm

    X_L = left_coord[0]
    X_R = right_coord[0]
    z = focal_length * baseline / (float(X_L - X_R))

    x_l = X_L * pixel_width
    x_r = X_R * pixel_width
    y_l = Y_L * pixel_height
    y_r = Y_R * pixel_height
    
    return [x_l * z / focal_length, y_l * z / focal_length, z]


def scale_2d_attribute(attribute, z_val):
    return attribute*(z_val+1)**2

