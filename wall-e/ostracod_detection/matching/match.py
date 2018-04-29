from ostracod_detection.locating import locator
import numpy as np

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

    def build_lists(self, ostracod_list, brightness_list, area_list, location_list):
        for o in ostracod_list:
            brightness_list.append(o.brightness)
            area_list.append(o.area)
            location_list.append(o.location[1])


    def set_variance(self, ostracod_list1, ostracod_list2):
        brightness = []
        area = []
        location = []   # y coordinates only
        self.build_lists(ostracod_list1, brightness, area, location)
        self.build_lists(ostracod_list2, brightness, area, location)
        self.brightness = np.var(brightness, dtype=np.float64)
        self.area = np.var(area, dtype=np.float64)
        self.location = np.var(location, dtype=np.float64)


def compute_dist(ostracod1, ostracod2, variance):
    b_sq = np.power(ostracod1.brightness - ostracod2.brightness, 2)
    a_sq = np.power(ostracod1.area - ostracod2.area, 2)
    l_sq = np.power(ostracod1.location[1] - ostracod2.location[1], 4)
    b_normalized = b_sq/variance.brightness
    a_normalized = a_sq/variance.area
    l_normalized = l_sq/variance.location
    sum = a_normalized + b_normalized + l_normalized
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
        ostracod_list1[i].matches.append(min_index)
        ostracod_list2[min_index].matches.append(i)


def match(left_filename, right_filename):
    ostracod_list_l = locator.get_ostracods(left_filename)
    ostracod_list_r = locator.get_ostracods(right_filename)
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
    match("../../../images/ostracod.png", "../../../images/ostracod.png")


if __name__ == '__main__':
    main()