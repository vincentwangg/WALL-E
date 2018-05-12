import math
import numpy as np
from pulse_data import FramePulseData
from pulse_data import PulseData
from camera import Camera
import sys

#TODO: implement get_z_val()

def depth_map(ostracod_list_l, ostracod_list_r, framepulsedata, framenum, camera):
    if not isinstance(framepulsedata, FramePulseData):
        sys.exit("fpd must be of type FramePulseData")
    if not isinstance(camera, Camera):
        sys.exit("camera must be of type Camera")
    for o in ostracod_list_l:
        if len(o.matches) > 0:
            pd = generate_pulse_data(o, ostracod_list_r[o.matches[0][0]], camera)
            if pd is not None:
                framepulsedata.add_pulse_to_frame(framenum, pd)


def generate_pulse_data(ostracod_l, ostracod_r, camera):
    avg_brightness = (ostracod_l.brightness + ostracod_r.brightness) / 2
    avg_area = (ostracod_l.area + ostracod_r.area) / 2
    print "ostracod_l location:", ostracod_l.location, "ostracod_r location", ostracod_r.location
    location = get_coord(ostracod_l.location, ostracod_r.location, camera.focal_length, camera.baseline)

    z = location[2]

    if z < 0:
        return

    brightness = avg_brightness/255
    area = scale_2d_attribute(avg_area, z)
    radius = (area/math.pi)**0.5
    return PulseData(xyz_coord=location, radius=radius, brightness=brightness)


def get_coord(left_coord, right_coord, focal_length, baseline):
    # hardcode pixel widths
    pixel_width = 0.0084 #mm
    pixel_height = 0.0098 #mm

    X_L, X_R, _ = left_coord - np.array([320, 239, 0])
    Y_L, Y_R, _ = right_coord - np.array([320, 239, 0])
    z = focal_length * baseline / (float(X_L - X_R))

    x_l = X_L * pixel_width
    y_l = Y_L * pixel_height
    
    return [x_l * z / focal_length, y_l * z / focal_length, z]


def scale_2d_attribute(attribute, z_val):
    return attribute*(z_val+1)**2

