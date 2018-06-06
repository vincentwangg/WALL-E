import numpy as np
import time
import math
import sys
import cv2

def frame_correct(l_file_name, r_file_name, offset):
  """Creates video of corrected and original video feeds displayed side by side
    
    :param l_file_name: File name of left video feed
    :param r_file_name: File name of right video feed
    :param offset: Offset of right feed 
    :return: None
    """
  l_feed = cv2.VideoCapture(l_file_name)
  r_feed = cv2.VideoCapture(r_file_name)
  fourcc = cv2.VideoWriter_fourcc(*'MJPG')
  _, frame = l_feed.read()
  (h, w, _) = frame.shape
  corrected = cv2.VideoWriter('corrected.mkv', fourcc, 30, (w, 2 + h * 2), True)
  if (offset < 0):
    r_feed.set(1, -offset)
    l_feed.set(1, 0)
  else:
    r_feed.set(1, 0)
    l_feed.set(1, offset)
  l_success, l_frame = l_feed.read()
  r_success, r_frame = r_feed.read()
  while (l_success and r_success):
    frame = np.zeros([2 + h * 2, w, 3])
    frame[:h, :, :] = l_frame
    frame[h:h + 2, :, :].fill(255)
    frame[h + 2:, :, :] = r_frame
    corrected.write(np.uint8(frame))
    l_success, l_frame = l_feed.read()
    r_success, r_frame = r_feed.read()
  corrected.release()

  l_feed.set(1, 0)
  r_feed.set(1, 0)
  corrected = cv2.VideoWriter('original.mkv', fourcc, 30, (w, 2 + h * 2), True)
  l_success, l_frame = l_feed.read()
  r_success, r_frame = r_feed.read()
  while (l_success and r_success):
    frame = np.zeros([2 + h * 2, w, 3])
    frame[:h, :, :] = l_frame
    frame[h:h + 2, :, :].fill(255)
    frame[h + 2:, :, :] = r_frame
    corrected.write(np.uint8(frame))
    l_success, l_frame = l_feed.read()
    r_success, r_frame = r_feed.read()
  corrected.release()
  l_feed.release()
  r_feed.release()

def main():
  start = time.time()
  if (len(sys.argv) != 4):
    print('Usage: python offset_vid_gen.py <l_feed> <r_feed> <offset>')
    exit()
  frame_correct(sys.argv[1], sys.argv[2], int(sys.argv[3]))

if __name__ == '__main__':
    main()
