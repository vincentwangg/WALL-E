import numpy as np
import cv2
import argparse
from locator import get_ostracods
from temporal_ostracod import TemporalOstracod

CENTROID_MAX_DIST = 15

def gen_ostracods(feed_file_name):
  temp_ostracods = {}  #dictionary to keep track of all the ostracods
  feed = cv2.VideoCapture(feed_file_name)
  success, frame = feed.read()
  prev_frame_ostracods = {}  # all the ostracods in the previous frame
  frame_no = 0
  while (success):   
    curr_ostracods = get_ostracods(frame)
    if frame_no == 0:
      for o in curr_ostracods:
        temp_ostracod = TemporalOstracod(o.location, o.area, frame_no)
        temp_ostracods[temp_ostracod.id] = temp_ostracod
        prev_frame_ostracods[temp_ostracod.id] = o
      frame_no = 1
      continue
    curr_frame_ostracods = {}
    for o in curr_ostracods:
      found_ostracod = False
      for key, o_prev in prev_frame_ostracods.items():
        if (is_same_ostracod(o, o_prev)):
          temp_ostracods[key].num_frames = temp_ostracods[key].num_frames + 1
          curr_frame_ostracods[key] = o
          found_ostracod = True
          break
      if not found_ostracod:
        temp_ostracod = TemporalOstracod(o.location, o.area, frame_no)
        temp_ostracods[temp_ostracod.id] = temp_ostracod
        curr_frame_ostracods[temp_ostracod.id] = o
    frame_no = frame_no + 1
    prev_frame_ostracods = curr_frame_ostracods
    success, frame = feed.read()
  feed.release()
  return prune_ostracod_list(temp_ostracods.values())

def prune_ostracod_list(temp_ostracods):
  pruned_list = []
  for o in temp_ostracods:
    if (o.num_frames > 3):
      pruned_list.append(o)
  return pruned_list

def is_same_ostracod(ost1, ost2):
  return np.sqrt(np.power((ost1.location[0] - ost2.location[0]), 2) \
    + np.power((ost1.location[1] - ost2.location[1]), 2)) < CENTROID_MAX_DIST
  # is_valid_area = abs(ost1.area - ost2.area) < MAX_AREA_DIFF
  # return is_valid_area and is_valid_distance


def main():
  parser = argparse.ArgumentParser(description='Find Ostracods (Temporal)')
  parser.add_argument('feed', type=str, help='file name of feed')

  args = parser.parse_args()

  ostracods = gen_ostracods(args.feed)

  print(ostracods)

if __name__ == '__main__':
    main()
