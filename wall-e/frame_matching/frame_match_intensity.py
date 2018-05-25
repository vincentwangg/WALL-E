import numpy as np
import time
import math
import sys
import cv2
import matplotlib.pyplot as plt


def get_gradient_diff(l_gradient, r_gradient, gradient_len, offset):
    diff = abs(l_gradient - np.roll(r_gradient, offset))[max(0, offset):min(gradient_len, gradient_len + offset)]
    diff /= float(len(diff))
    return np.sum(diff)


def get_optimal_offset(l_gradient, r_gradient, max_offset):
    min_diff = sys.maxint
    gradient_len = len(l_gradient)
    if len(r_gradient) > gradient_len:
        r_gradient = r_gradient[0:gradient_len]
    else:
        l_gradient = l_gradient[0:len(r_gradient)]
        gradient_len = len(r_gradient)
    print(len(l_gradient))
    print(len(r_gradient))
    optimal_offset = 0
    for offset in range(-max_offset, max_offset + 1):
        curr_diff = get_gradient_diff(l_gradient, r_gradient, gradient_len, offset)
        if curr_diff < min_diff:
            min_diff = curr_diff
            optimal_offset = offset
    return optimal_offset


def calculate_gradient(file_name, is_left_gradient, fraction):
    feed = cv2.VideoCapture(file_name)

    prev_frame = cv2.cvtColor(feed.read()[1], cv2.COLOR_BGR2GRAY)
    num_pixels = int(math.floor(prev_frame.shape[1] - (prev_frame.shape[1] * fraction)))
    if is_left_gradient:
        prev_frame = prev_frame[:, num_pixels:]
    else:
        prev_frame = prev_frame[:, :(prev_frame.shape[1] - num_pixels)]
    x, prev_frame = cv2.threshold(prev_frame, 110, 255, cv2.THRESH_TOZERO)
    normal_factor = float(1) / (prev_frame.shape[0] * prev_frame.shape[1])
    num_frames = int(feed.get(cv2.CAP_PROP_FRAME_COUNT))
    idx = 0
    gradient = np.empty(num_frames - 1)
    while idx < num_frames - 1 and feed.isOpened():
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        prog = 100 * idx / (num_frames - 2)
        sys.stdout.write('\r{0}% - [{1}{2}]'.format(prog, '*' * prog, ' ' * (100 - prog)))
        sys.stdout.flush()
        succ, frame = feed.read()
        if frame is not None:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            if is_left_gradient:
                frame = frame[:, num_pixels:]
            else:
                frame = frame[:, :(prev_frame.shape[1])]
            x, frame = cv2.threshold(frame, 150, 255, cv2.THRESH_TOZERO)
            if idx == 0:
                gradient[idx] = normal_factor * np.sum(abs(frame - prev_frame))
            else:
                gradient[idx] = (0.6 * gradient[idx - 1]) + (0.4 * normal_factor * np.sum(abs(frame - prev_frame)))
        idx = idx + 1
    feed.release()
    return gradient


def plot_intensity_curves(l_gradient, r_gradient):
    plt.plot(l_gradient, 'g')
    plt.plot(r_gradient, 'r')
    plt.ylabel('dI')
    plt.xlabel('frame number')
    plt.show()


def compare_feeds(l_file_name, r_file_name, l_gradient, offset):
    frame_no = np.argmax(l_gradient)
    l_feed = cv2.VideoCapture(l_file_name)
    l_feed.set(1, frame_no - 2)
    frame = cv2.cvtColor(l_feed.read()[1], cv2.COLOR_BGR2GRAY)
    (height, width) = frame.shape
    l_five_image_seq = np.zeros([height, width * 5 + 8])
    l_five_image_seq.fill(255)
    l_five_image_seq[:, 0:width] = frame
    curr = width + 2
    for i in range(0, 4):
        l_five_image_seq[:, curr:(curr + width)] = cv2.cvtColor(l_feed.read()[1], cv2.COLOR_BGR2GRAY)
        curr += width + 2
    cv2.imwrite("l_feed_frames.jpg", l_five_image_seq)

    r_feed = cv2.VideoCapture(r_file_name)
    r_feed.set(1, frame_no - 2 + offset)
    frame = cv2.cvtColor(r_feed.read()[1], cv2.COLOR_BGR2GRAY)
    (height, width) = frame.shape
    r_five_image_seq = np.zeros([height, width * 5 + 8])
    r_five_image_seq.fill(255)
    r_five_image_seq[:, 0:width] = frame
    curr = width + 2
    for i in range(0, 4):
        r_five_image_seq[:, curr:(curr + width)] = cv2.cvtColor(r_feed.read()[1], cv2.COLOR_BGR2GRAY)
        curr += width + 2
    cv2.imwrite("r_feed_frames.jpg", r_five_image_seq)


def main():
    start = time.time()
    if len(sys.argv) != 3:
        print('Usage: python frame_match_intensity.py <left_feed> <right_feed>')
        exit()
    print 'left feed gradient calculating...'
    l_gradient = calculate_gradient(sys.argv[1], True, 0.8)
    print '\nright feed gradient calculating...'
    r_gradient = calculate_gradient(sys.argv[2], False, 0.8)
    opt = get_optimal_offset(l_gradient, r_gradient, 200)
    print '\nOptimal right feed offset:', opt
    print 'Time elapsed:', (time.time() - start) / 60, 'minutes'
    plot_intensity_curves(l_gradient, r_gradient)
    compare_feeds(sys.argv[1], sys.argv[2], l_gradient, opt)


if __name__ == '__main__':
    main()
