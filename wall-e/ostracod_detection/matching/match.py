from ostracod_detection.locating import locator
import numpy as np
from cv2 import imread

# given two lists of ostracods with attributes:
    # (x,y) location
    # brightness
    # area

# match up the corresponding ostracods in each list


class Variance:
    def __init__(self):
        self.brightness = None
        self.area = None
        self.location = None
        self.distance_from_mean = None

    def build_lists(self, ostracod_list, brightness_list, area_list, location_list, distance_from_mean):
        for o in ostracod_list:
            brightness_list.append(o.brightness)
            area_list.append(o.area)
            location_list.append(o.location[1])
            distance_from_mean.append(o.distance_from_mean)


    def set_variance(self, ostracod_list1, ostracod_list2):
        brightness = []
        area = []
        location = []   # y coordinates only
        distance_from_mean = []
        self.build_lists(ostracod_list1, brightness, area, location, distance_from_mean)
        self.build_lists(ostracod_list2, brightness, area, location, distance_from_mean)
        self.brightness = np.var(brightness, dtype=np.float64)
        self.area = np.var(area, dtype=np.float64)
        self.location = np.var(location, dtype=np.float64)
        self.distance_from_mean = np.var(distance_from_mean, dtype=np.float64)


def compute_dist(ostracod1, ostracod2, variance):
    b_sq = np.power(ostracod1.brightness - ostracod2.brightness, 2)
    a_sq = np.power(ostracod1.area - ostracod2.area, 2)
    l_sq = np.power(ostracod1.location[1] - ostracod2.location[1], 4)
    d_m_sq = np.power(ostracod1.distance_from_mean - ostracod2.distance_from_mean, 2)
    b_normalized = b_sq/variance.brightness
    a_normalized = a_sq/variance.area
    l_normalized = l_sq/variance.location
    d_m_normalized = d_m_sq/variance.distance_from_mean
    sum = a_normalized + b_normalized + l_normalized + d_m_normalized
    dist = np.power(sum, 0.5)
    return dist


def get_matching_pairs(ostracod_list1, ostracod_list2): # ostracod_list1 must be smaller or equal to ostracod_list2
    variance = Variance()
    variance.set_variance(ostracod_list1, ostracod_list2)
    for i in xrange(len(ostracod_list1)):
        min_index = 0
        min_val = compute_dist(ostracod_list1[i], ostracod_list2[0], variance)
        for j in xrange(1, len(ostracod_list2)):
            dist = compute_dist(ostracod_list1[i], ostracod_list2[j], variance)
            if dist < min_val:
                min_index = j
                min_val = dist
        ostracod_list1[i].matches.append((min_index, min_val))
        ostracod_list2[min_index].matches.append((i, min_val))


def match(image_l, image_r):
    ostracod_list_l = locator.get_ostracods(image_l)
    ostracod_list_r = locator.get_ostracods(image_r)
    if len(ostracod_list_r) < len(ostracod_list_l):
        get_matching_pairs(ostracod_list_r, ostracod_list_l)
    else:
        get_matching_pairs(ostracod_list_l, ostracod_list_r)

    print "matches of left: "
    print_matches(ostracod_list_l)
    print "matches of right: "
    print_matches(ostracod_list_r)

    return ostracod_list_l, ostracod_list_r


def print_matches(ostracod_list):
    for i in xrange(len(ostracod_list)):
        print i, ostracod_list[i].matches


def main():
    image_l = imread("../../../images/ostracod.png")
    image_r = imread("../../../images/ostracod.png")
    match(image_l, image_r)


if __name__ == '__main__':
    main()
