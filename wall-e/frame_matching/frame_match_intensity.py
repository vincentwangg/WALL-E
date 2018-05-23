import numpy as np
import time
import math
import sys
import cv2
import argparse
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt

def get_gradient_diff(l_gradient, r_gradient, gradient_len, offset):
  diff = abs(l_gradient - np.roll(r_gradient, offset))[max(0, offset):min(gradient_len, gradient_len + offset)]
  diff /= float(len(diff))
  return np.sum(diff)

def get_optimal_offset(l_gradient, r_gradient, max_offset):
  min_diff = sys.maxint
  gradient_len = len(l_gradient)
  if (len(r_gradient) > gradient_len):
    r_gradient = r_gradient[0:gradient_len]
  else:
    l_gradient = l_gradient[0:len(r_gradient)]
    gradient_len = len(r_gradient)
  optimal_offset = 0
  for offset in range(-max_offset, max_offset + 1):
    curr_diff = get_gradient_diff(l_gradient, r_gradient, gradient_len, offset)
    if curr_diff < min_diff:
      min_diff = curr_diff
      optimal_offset = offset
  return optimal_offset

def calculate_gradient(file_name, start_frame, end_frame):
  feed = cv2.VideoCapture(file_name)
  feed.set(1, start_frame)

  num_frames = end_frame - start_frame

  prev_frame = cv2.cvtColor(feed.read()[1], cv2.COLOR_BGR2GRAY)
  _, prev_frame = cv2.threshold(prev_frame, 150, 255, cv2.THRESH_TOZERO)
  idx = 0
  gradient = np.empty(num_frames - 1)

  while idx < num_frames - 1 and feed.isOpened():
    success, frame = feed.read()
    if not success:
      break

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, frame = cv2.threshold(frame, 150, 255, cv2.THRESH_TOZERO)

    gradient[idx] = np.sum(abs(frame - prev_frame))

    idx = idx + 1
  feed.release()
  return gradient

def plot_intensity_curves(l_gradient, r_gradient):
  plt.plot(l_gradient, 'g')
  plt.plot(r_gradient, 'r')
  plt.ylabel('dI')
  plt.xlabel('frame number')
  plt.show()

def compare_feeds(l_file_name, r_file_name, l_gradient, l_offset, r_offset):
  frame_no = np.argmax(l_gradient)
  l_feed = cv2.VideoCapture(l_file_name)
  l_feed.set(1, frame_no - 3 + l_offset)
  frame = cv2.cvtColor(l_feed.read()[1], cv2.COLOR_BGR2GRAY)
  (height, width) = frame.shape
  l_five_image_seq = np.zeros([height, width * 5 + 8])
  l_five_image_seq.fill(255)
  l_five_image_seq[:, 0:width] = frame
  curr = width + 2
  for i in range(0, 4):
    l_five_image_seq[:, curr:(curr + width)] = cv2.cvtColor(l_feed.read()[1], cv2.COLOR_BGR2GRAY)
    curr += width + 2
  cv2.imwrite('l_feed_frames.jpg', l_five_image_seq);

  r_feed = cv2.VideoCapture(r_file_name)
  r_feed.set(1, frame_no - 3 + r_offset)
  frame = cv2.cvtColor(r_feed.read()[1], cv2.COLOR_BGR2GRAY)
  (height, width) = frame.shape
  r_five_image_seq = np.zeros([height, width * 5 + 8])
  r_five_image_seq.fill(255)
  r_five_image_seq[:, 0:width] = frame
  curr = width + 2
  for i in range(0, 4):
    r_five_image_seq[:, curr:(curr + width)] = cv2.cvtColor(r_feed.read()[1], cv2.COLOR_BGR2GRAY)
    curr += width + 2
  cv2.imwrite('r_feed_frames.jpg', r_five_image_seq);

def frame_match(left_file_name, right_file_name, start_timestamp, end_timestamp):  # timestamps in seconds
  start_frame = start_timestamp * 30 if start_timestamp else 0
  end_frame =   end_timestamp * 30 if end_timestamp else -1

  print('left feed gradient calculating...')
  l_gradient = calculate_gradient(left_file_name, start_frame, end_frame) if end_timestamp else calculate_gradient(args.left_feed, start_frame)
  print('right feed gradient calculating...')
  r_gradient = calculate_gradient(right_file_name, start_frame, end_frame) if end_timestamp else calculate_gradient(args.right_feed, start_frame)

  opt = get_optimal_offset(l_gradient, r_gradient, 50)
  l_offset = 0 if opt > 0 else -opt
  r_offset = opt if opt > 0 else 0

  print('left feed offset: ' + str(l_offset) + ' frames')
  print('right feed offset: ' + str(r_offset) + ' frames')
  return l_offset, r_offset, l_gradient, r_gradient

def main():
  parser = argparse.ArgumentParser(description='Frame match two videos')
  parser.add_argument('left_feed', type=str, help='file name of left feed')
  parser.add_argument('right_feed', type=str, help='file name of right feed')
  parser.add_argument('--start_timestamp', type=int, help='timestamp of clip beginning in seconds')
  parser.add_argument('--end_timestamp', type=int, help='timestamp of clip end in seconds')

  args = parser.parse_args()

  l_offset, r_offset, l_gradient, r_gradient = frame_match(args.left_feed, args.right_feed, args.start_timestamp, args.end_timestamp)

  plot_intensity_curves(l_gradient, r_gradient)
  compare_feeds(sys.argv[1], sys.argv[2], l_gradient, l_offset, r_offset)

if __name__ == '__main__':
    main()
