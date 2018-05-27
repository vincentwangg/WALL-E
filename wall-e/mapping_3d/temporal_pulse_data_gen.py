from pulse_data import FramePulseData
from pulse_data import PulseData
import math

# radius ostracods are detected at
thresh_r = 4

def gen_frame_pulse_data(matched_ostracod_list):
    fpd = FramePulseData()
    for o in matched_ostracod_list:
        init_r = math.sqrt(o.area / pi)
        delt_r = (init_r - thresh_r) / o.num_frames
        num_frames = int(init_r / delt_r)
        for x in range(num_frames):
            fpd.add_pulse_to_frame(o.frame_start + x,
                         PulseData(o.location, init_r - (x * delt_r), brightness=1))