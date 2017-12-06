import numpy as np
import time
import math
import sys
import cv2

def denoise(file_name):
  feed = cv2.VideoCapture(file_name)
  moving_average = feed.read()[1]
  num_frames = int(feed.get(cv2.CAP_PROP_FRAME_COUNT))
  fourcc = cv2.VideoWriter_fourcc(*'MJPG')
  (h, w) = moving_average.shape[:2]
  writer = cv2.VideoWriter('denoise_' + file_name.split('.')[0] + '.mkv', fourcc, 30, (w, h), True)
  writer.write(np.uint8(moving_average))
  count = 1
  while (count < num_frames and feed.isOpened()):
    moving_average = (0.9 * moving_average) + (0.1 * feed.read()[1])
    writer.write(np.uint8(moving_average)) 
    prog = 100 * count / (num_frames - 1)
    sys.stdout.write('\r{0}% - [{1}{2}]'.format(prog, '*' * prog, ' ' * (100 - prog)))
    sys.stdout.flush()
    count += 1
  feed.release()
  writer.release()

def main():
  start = time.time()
  if (len(sys.argv) != 2):
    print('Usage: python3 denoise.py <feed>')
    exit()
  denoise(sys.argv[1])

if __name__ == '__main__':
    main()