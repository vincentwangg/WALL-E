from ostracod_detection.locating.locator import Ostracod
import numpy as np

class Camera:
    def __init__(self, focal_length, baseline):
        self.focal_length = focal_length
        self.baseline = baseline


def depth_map(ostracod_list1, ostracod_list2):
    blender_list = []
    for o in ostracod_list1:
        if len(o.matches) > 0:
            blender_o = generate_blender_ostracod(o, ostracod_list2[o.matches[0][0]])
            blender_list.append(blender_o)
    return blender_list


def generate_blender_ostracod(ostracod1, ostracod2):
    avg_brightness = (ostracod1.brightness + ostracod2.brightness)/2
    avg_area = (ostracod1.area + ostracod2.area)/2
    location = [ostracod1.location[0], ostracod1.location[1]]
    z = 0 # to be get_x_Val() or something
    location.append(z)
    brightness = scale_attribute(avg_brightness, z)
    area = scale_attribute(avg_area, z)
    radius = np.power(area/np.pi, 0.5)
    return [location, radius, brightness]


def scale_attribute(attribute, z_val):
    return attribute*np.power(z_val+1, 2)


def main():
    print "stub"


if __name__ == '__main__':
    main()