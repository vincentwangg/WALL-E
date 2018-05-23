import math
import numpy as np
from pulse_data import FramePulseData
from pulse_data import PulseData
from camera import Camera
import sys

# radius ostracods are detected at
THRESH_R = 4

def depth_map(ostracod_pairs, frame_pulse_data, camera):
    if not isinstance(frame_pulse_data, FramePulseData):
        sys.exit("fpd must be of type FramePulseData")
    if not isinstance(camera, Camera):
        sys.exit("camera must be of type Camera")
    matched_ostracod_list = []
    for o in ostracod_pairs:
        matched_ostracod_list.append(get_mapped_ostracod(o[0], o[1], camera))
    gen_frame_pulse_data(matched_ostracod_list, frame_pulse_data)


def get_mapped_ostracod(ostracod_l, ostracod_r, camera):
    avg_brightness = (ostracod_l.brightness + ostracod_r.brightness) / 2
    avg_area = (ostracod_l.area + ostracod_r.area) / 2
    print "ostracod_l location:", ostracod_l.location, "ostracod_r location", ostracod_r.location
    location = get_coord(ostracod_l.location, ostracod_r.location, camera.focal_length, camera.baseline)

    z = location[2]

    if z < 0:
        return

    brightness = avg_brightness/255
    area = scale_2d_attribute(avg_area, z)

    return TemporalOstracod(location, area, ostracod_l.frame_start)


def get_coord(left_coord, right_coord, focal_length, baseline):
    X_L, X_R, _ = left_coord - np.array([320, 239, 0])
    Y_L, Y_R, _ = right_coord - np.array([320, 239, 0])
    z = focal_length * baseline / (float(X_L - X_R))
    
    return [X_l * z / focal_length, Y_l * z / focal_length, z]

def gen_frame_pulse_data(matched_ostracod_list, frame_pulse_data):
    for o in matched_ostracod_list:
        init_r = (o.area / pi) ** 0.5
        delt_r = (init_r - THRESH_R) / o.num_frames
        num_frames = int(init_r / delt_r)
        for x in range(num_frames):
            frame_pulse_data.add_pulse_to_frame(o.frame_start + x,
                         PulseData(o.location, init_r - (x * delt_r), brightness=1))

