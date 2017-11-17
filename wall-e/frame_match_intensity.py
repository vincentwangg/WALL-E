import numpy as np
import time
import sys
import cv2
import matplotlib.pyplot as plt

def get_gradient_diff(l_gradient, r_gradient, offset):
  gradient_len = len(l_gradient)
  diff = abs(l_gradient - np.roll(r_gradient, offset))[max(0, offset):min(gradient_len, gradient_len + offset)]
  diff /= float(len(diff))
  return np.sum(diff)

def get_optimal_offset(l_gradient, r_gradient, max_offset):
  min_diff = sys.maxint
  optimal_offset = 0
  for offset in range(-max_offset, max_offset + 1):
    curr_diff = get_gradient_diff(l_gradient, r_gradient, offset)
    if curr_diff < min_diff:
      min_diff = curr_diff
      optimal_offset = offset
  return optimal_offset

def calculate_gradient(file_name):
  feed = cv2.VideoCapture(file_name)

  prev_frame = cv2.cvtColor(feed.read()[1], cv2.COLOR_BGR2GRAY)
  x, prev_frame = cv2.threshold(prev_frame, 150, 255, cv2.THRESH_BINARY)
  num_frames = int(feed.get(cv2.CAP_PROP_FRAME_COUNT))
  idx = 0
  gradient = np.empty(num_frames - 1)
  while idx < num_frames - 1 and feed.isOpened():
      if cv2.waitKey(1) & 0xFF == ord('q'):
          break
      prog = 100 * idx / (num_frames - 2)
      sys.stdout.write('\r{0}% - [{1}{2}]'.format(prog, '*' * prog, ' ' * (100 - prog)))
      sys.stdout.flush()
      frame = cv2.cvtColor(feed.read()[1], cv2.COLOR_BGR2GRAY)
      x, frame = cv2.threshold(frame, 150, 255, cv2.THRESH_BINARY)
      gradient[idx] = np.sum(abs((frame - prev_frame)))
      idx = idx + 1
  feed.release()
  return gradient

def plot_intensity_curves(l_gradient, r_gradient):
  plt.plot(l_gradient, 'g')
  plt.plot(r_gradient, 'r')
  plt.ylabel('dI')
  plt.xlabel('frame number')
  plt.show()

def main():
  start = time.time()
  if (len(sys.argv) != 3):
    print('Usage: python3 frame_match_intensity.py <left_feed> <right_feed>')
    exit()
  print 'left feed gradient calculating...'
  l_gradient = calculate_gradient(sys.argv[1])
  print '\nright feed gradient calculating...'
  r_gradient = calculate_gradient(sys.argv[2])
  plot_intensity_curves(l_gradient, r_gradient)
  opt = get_optimal_offset(l_gradient, r_gradient, 200)
  print '\nOptimal right feed offset:', opt
  print 'Time elapsed:', (time.time() - start) / 60, 'minutes'

if __name__ == '__main__':
    main()
