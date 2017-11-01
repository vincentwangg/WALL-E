import numpy as np
import sys
import cv2

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

def calculate_gradient(file_name, start_frame, num_frames):
  feed = cv2.VideoCapture(file_name)

  feed.set(cv2.CAP_PROP_POS_FRAMES, start_frame);
  prev_frame = cv2.cvtColor(feed.read()[1], cv2.COLOR_BGR2GRAY)
  x, prev_frame = cv2.threshold(prev_frame, 150, 255, cv2.THRESH_BINARY)
  total_count = float(feed.get(cv2.CAP_PROP_FRAME_COUNT))
  idx = 0
  gradient = np.empty(num_frames)
  while idx < num_frames and feed.isOpened():
      prog = 100 * idx / (num_frames - 1)
      sys.stdout.write('\r{0}% - [{1}{2}]'.format(prog, '*' * prog, ' ' * (100 - prog)))
      sys.stdout.flush()
      frame = cv2.cvtColor(feed.read()[1], cv2.COLOR_BGR2GRAY)
      x, frame = cv2.threshold(frame, 150, 255, cv2.THRESH_BINARY)
      gradient[idx] = np.sum(abs((frame - prev_frame)))
      idx = idx + 1
      if cv2.waitKey(1) & 0xFF == ord('q'):
          break
  feed.release()
  return gradient

def main():
  if (len(sys.argv) != 3):
    print('Usage: python3 frame_match_intensity.py <left_feed> <right_feed>')
    exit()
  print 'left feed gradient calculating...'
  l_gradient = calculate_gradient(sys.argv[1], 0, 25240)
  print '\nright feed gradient calculating...'
  r_gradient = calculate_gradient(sys.argv[2], 0, 25240)
  opt = get_optimal_offset(l_gradient, r_gradient, 200)
  print '\nOptimal right feed offset:', opt 

if __name__ == '__main__':
    main()
