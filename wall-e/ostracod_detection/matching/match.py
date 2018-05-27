from ostracod_detection.locating import locator
import numpy as np
from cv2 import imread

# given two lists of ostracods with attributes:
    # (x,y) location
    # brightness
    # area

# match up the corresponding ostracods in each list

class Variance:
    def __init__(self, ostracod_list1, ostracod_list2):
        self.brightness = None
        self.area = None
        self.location = None
        self.set_variance(ostracod_list1, ostracod_list2)

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

# ostracod_list1 must be smaller or equal to ostracod_list2
# the indexes_lists include indexes that have not been matched yet

def get_pairs_with_duplicates(ostracod_list1, indexes_list1, ostracod_list2, indexes_list2, variance):
    for i in indexes_list1:
        min_index = indexes_list2[0]
        min_val = compute_dist(ostracod_list1[i], ostracod_list2[indexes_list2[0]], variance)
        for j in indexes_list2:
            dist = compute_dist(ostracod_list1[i], ostracod_list2[j], variance)
            if dist < min_val:
                min_index = j
                min_val = dist
        ostracod_list1[i].matches.append((min_index, min_val))
        ostracod_list2[min_index].matches.append((i, min_val))


# takes in a list of matches and eliminates all of the values except the best match
# it returns all of the indexes eliminated, so that they can be rematched

def eliminate_duplicates(matches):
    min_val = matches[0][1]
    unmatched_list = []
    length = len(matches)
    while length > 1:
        if matches[1][1] < min_val:
            min_val = matches[1][1]
            unmatched = matches.pop(0)
        else:
            unmatched = matches.pop(1)
        unmatched_list.append(unmatched[0])
        length -= 1
    return unmatched_list


# takes in the indexes that need to be matched in the second list and returns the duplicates no_matches
# ostracod_list1 will never have more than one match per ostracod because it is the smaller list
# It simply iterates over ostracod_list2 and removes matches from ostracod_list1 that have been matched incorrectly

def build_new_index_lists(ostracod_list1, ostracod_list2, indexes_list2):
    no_matches = []
    duplicates = []
    for i in indexes_list2:
        num_matches = len(ostracod_list2[i].matches)
        if num_matches == 0:
            no_matches.append(i)
        elif num_matches > 1:
            duplicates += eliminate_duplicates(ostracod_list2[i].matches)
    for i in duplicates:
        ostracod_list1[i].matches = []
    return duplicates, no_matches


# gets matching pairs while handling duplicates

def get_matching_pairs(ostracod_list1, ostracod_list2): # ostracod_list1 must be smaller or equal to ostracod_list2
    indexes_list1 = range(len(ostracod_list1))
    indexes_list2 = range(len(ostracod_list2))
    variance = Variance(ostracod_list1, ostracod_list2)
    while len(indexes_list1) > 0:
        get_pairs_with_duplicates(ostracod_list1, indexes_list1, ostracod_list2, indexes_list2, variance)
        indexes_list1, indexes_list2 = build_new_index_lists(ostracod_list1, ostracod_list2, indexes_list2)


# removes matches if they have a distance value of greater than the threshold value
# a match is a list of tuples (match_index, match_value)
# this should only be called if each ostracod only has one match, it does not handle multiple matches per ostracod

def threshold_matches(ostracod_list_l, ostracod_list_r, threshold_value):
    for o in ostracod_list_l:
        for m in o.matches:
            if m[1] > threshold_value:
                ostracod_list_r[m[0]].matches = []
                o.matches = []
                break


def match(ostracod_list_l, ostracod_list_r, threshold):
    if len(ostracod_list_r) < len(ostracod_list_l):
        get_matching_pairs(ostracod_list_r, ostracod_list_l)
    else:
        get_matching_pairs(ostracod_list_l, ostracod_list_r)

    threshold_matches(ostracod_list_l, ostracod_list_r, threshold)

    # print "matches of left: "
    # print_matches(ostracod_list_l)
    # print "matches of right: "
    # print_matches(ostracod_list_r)

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
