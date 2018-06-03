import math
import numpy as np
from pulse_data import FramePulseData
from pulse_data import PulseData
from camera import Camera
from ostracod_detection.locating.temporal_ostracod import TemporalOstracod
import sys

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
    avg_area = (ostracod_l.area + ostracod_r.area) / 2
    location = get_coord(ostracod_l.location, ostracod_r.location, camera.focal_length, camera.baseline)

    z = location[2]

    if z <= 0:
        return

    return TemporalOstracod(location, avg_area, ostracod_l.frame_start, num_frames \
            = max(ostracod_l.num_frames, ostracod_r.num_frames))


def get_coord(left_coord, right_coord, focal_length, baseline):
    X_L, Y_L, _ = left_coord - np.array([320, 239, 0])
    X_R, Y_R, _ = right_coord - np.array([320, 239, 0])

    if X_L - X_R == 0:
        return [0,0,0]

    z = focal_length * baseline / (float(X_L - X_R))
    
    return [X_L * z / focal_length, Y_L * z / focal_length, z]

def gen_frame_pulse_data(matched_ostracod_list, frame_pulse_data):
    for o in matched_ostracod_list:
        if o is None:
            continue
        init_r = (o.area / math.pi) ** 0.5
        delt_r = init_r / o.num_frames
        num_frames = o.num_frames
        for x in range(num_frames):
            frame_pulse_data.add_pulse_to_frame(o.frame_start + x,
                         PulseData(o.location, init_r - (x * delt_r), brightness=1))

# If you want to generate pulse data one frame at a time with no temporal data
def generate_pulse_data(ostracod_l, ostracod_r, camera):
    avg_brightness = (ostracod_l.brightness + ostracod_r.brightness) / 2
    avg_area = (ostracod_l.area + ostracod_r.area) / 2
    location = get_coord(ostracod_l.location, ostracod_r.location, camera.focal_length, camera.baseline)

    z = location[2]

    if z <= 0:
        return

    brightness = avg_brightness/255
    radius = (avg_area/math.pi)**0.5
    radius = radius * z/camera.focal_length

    return PulseData(xyz_coord=location, radius=radius, brightness=brightness)

# If you want to do a depth_map frame by frame without using temporal data
def depth_map_frame(ostracod_list_l, ostracod_list_r, framepulsedata, framenum, camera):
    if not isinstance(framepulsedata, FramePulseData):
        sys.exit("fpd must be of type FramePulseData")
    if not isinstance(camera, Camera):
        sys.exit("camera must be of type Camera")
    for o in ostracod_list_l:
        if len(o.matches) > 0:
            pd = generate_pulse_data(o, ostracod_list_r[o.matches[0][0]], camera)
            if pd is not None:
                framepulsedata.add_pulse_to_frame(framenum, pd)
