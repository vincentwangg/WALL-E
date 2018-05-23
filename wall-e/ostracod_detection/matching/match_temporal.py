import numpy as np
import sys
import cv2

def get_ostracod_matches(temp_ostracods_L, temp_ostracods_R):
	# indicates if right ostracod is already paired off
	is_used = [False] * len(temp_ostracods_R) 

	ostracod_pairs = []

	for o_l in temp_ostracods_L:
		candidate_ostracods = []
		for i in range(len(temp_ostracods_R)):
			if (is_used[i]):
				continue
			o_r = temp_ostracods_R[i]
			if abs(o_l.frame_start - o_r.frame_start) < 4:
				candidate_ostracods.append(i)
		num_matches = len(candidate_ostracods)
		if (num_matches == 0):
			continue
		if (num_matches == 1):
			match_index = candidate_ostracods[0]
			ostracod_pairs.append((o_l, temp_ostracods_R[match_index]))
			is_used[match_index] = True
			continue
		min_dist = sys.maxint
		match_index = None
		for i in candidate_ostracods:
			o_r = temp_ostracods_R[i]
			curr_dist = calc_dist(o_l, o_r)
			if (curr_dist < min_dist):
				match_index = i
				min_dist = curr_dist
		ostracod_pairs.append((o_l, temp_ostracods_R[match_index]))
		is_used[match_index] = True
	return ostracod_pairs


def calc_dist(ostracod_l, ostracod_r):
	return abs((ostracod_l.location[1]) - (ostracod_r.location[1]))
