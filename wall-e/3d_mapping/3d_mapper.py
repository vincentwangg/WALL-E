from ostracod_detection.locating.locator import Ostracod

class Camera:
    def __init__(self, focal_length, baseline):
        self.focal_length = focal_length
        self.baseline = baseline


def map(ostracod_list1, ostracod_list2):
    if len(ostracod_list1) < len(ostracod_list2):
        combined_ostracods = combine_lists(ostracod_list1, ostracod_list2)
    else:
        combined_ostracods = combine_lists(ostracod_list2, ostracod_list1)
    return combined_ostracods

def combine_lists(ostracod_list1, ostracod_list2):
    new_list = []
    for o in ostracod_list1:
        combined_o = combine_ostracod(o, ostracod_list2[o.matches[0][0]])
        new_list.append(combined_o)
    return new_list

def combine_ostracod(ostracod1, ostracod2):
    avg_brightness = (ostracod1.brightness + ostracod2.brightness)/2
    avg_area = (ostracod1.area + ostracod2.area)/2
    location = [ostracod1.location[0], ostracod1.location[1]]
    z = 0
    location.append(z)
    return Ostracod(location, avg_area, avg_brightness)