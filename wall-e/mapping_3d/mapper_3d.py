import math
from pulse_data import FramePulseData
from pulse_data import PulseData
import sys


def depth_map(ostracod_list1, ostracod_list2, fpd, framenum):
    if not isinstance(fpd, FramePulseData):
        sys.exit("fpd must be of type FramePulseData")
    for o in ostracod_list1:
        if len(o.matches) > 0:
            pd = generate_pulse_data(o, ostracod_list2[o.matches[0][0]])
            fpd.add_pulse_to_frame(framenum, pd)


def generate_pulse_data(ostracod1, ostracod2):
    avg_brightness = (ostracod1.brightness + ostracod2.brightness)/2
    avg_area = (ostracod1.area + ostracod2.area)/2
    location = [ostracod1.location[0], ostracod1.location[1]]
    z = 0 # to be get_x_Val() or something
    location.append(z)
    brightness = scale_attribute(avg_brightness, z)
    area = scale_attribute(avg_area, z)
    radius = (area/math.pi)**0.5
    return PulseData(xyz_coord=location, radius=radius, brightness=brightness)


def scale_attribute(attribute, z_val):
    return attribute*(z_val+1)**2


def main():
    print "stub"


if __name__ == '__main__':
    main()