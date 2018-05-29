import argparse
import sys

import cv2
import matplotlib
import numpy as np

from gui.abstract_screens.utilities.constants import PROGRESS_SCREEN_PERCENT_DONE, PROGRESS_SCREEN_MESSAGE_LIST
from gui.pipeline1.utilities.constants import LEFT, RIGHT, TOTAL_FRAMES_KEY, FOUND_OPTIMAL_OFFSET_KEY, \
    LEFT_OFFSET_KEY, RIGHT_OFFSET_KEY
from utils_general.frame_calculations import calculate_video_scan_frame_information

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

    num_frames = int(feed.get(cv2.CAP_PROP_FRAME_COUNT)) if end_frame == -1 else end_frame - start_frame

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
    end_frame = end_timestamp * 30 if end_timestamp else -1

    print('left feed gradient calculating...')
    l_gradient = calculate_gradient(left_file_name, start_frame, end_frame)
    print('right feed gradient calculating...')
    r_gradient = calculate_gradient(right_file_name, start_frame, end_frame)

    opt = get_optimal_offset(l_gradient, r_gradient, 50)
    l_offset = 0 if opt > 0 else -opt
    r_offset = opt if opt > 0 else 0

    print('left feed offset: ' + str(l_offset) + ' frames')
    print('right feed offset: ' + str(r_offset) + ' frames')
    return l_offset, r_offset, l_gradient, r_gradient


def frame_match_gui_backend_logic(controller):
    start_frame = controller.frame_matching_frame_range.first_frame
    last_frame_inclusive = controller.frame_matching_frame_range.last_frame_inclusive

    first_frame_left, last_frame_left, first_frame_right, last_frame_right, num_frames_to_scan = \
        calculate_video_scan_frame_information(start_frame,
                                               last_frame_inclusive,
                                               controller.video_offsets.left_offset,
                                               controller.video_offsets.right_offset,
                                               controller.video_frame_loader)

    progress_dict = {LEFT: 0, RIGHT: 0, LEFT_OFFSET_KEY: 0, RIGHT_OFFSET_KEY: 0,
                     TOTAL_FRAMES_KEY: num_frames_to_scan - 2,
                     FOUND_OPTIMAL_OFFSET_KEY: False}

    update_ui(progress_dict, controller)

    l_gradient = calculate_gradient_gui_version(controller,
                                                controller.video_frame_loader.vc_left,
                                                first_frame_left,
                                                last_frame_left,
                                                num_frames_to_scan,
                                                LEFT,
                                                progress_dict)
    r_gradient = calculate_gradient_gui_version(controller,
                                                controller.video_frame_loader.vc_right,
                                                first_frame_right,
                                                last_frame_right,
                                                num_frames_to_scan,
                                                RIGHT,
                                                progress_dict)

    opt = get_optimal_offset(l_gradient, r_gradient, 50)
    l_offset = 0 if opt > 0 else -opt
    r_offset = opt if opt > 0 else 0

    progress_dict[FOUND_OPTIMAL_OFFSET_KEY] = True
    progress_dict[LEFT_OFFSET_KEY] = l_offset
    progress_dict[RIGHT_OFFSET_KEY] = r_offset
    update_ui(progress_dict, controller)

    controller.video_offsets.left_offset = l_offset
    controller.video_offsets.right_offset = r_offset


def update_ui(progress_dict, controller):
    left_video_percent_done = round(progress_dict[LEFT] * 100.0 / progress_dict[TOTAL_FRAMES_KEY])
    right_video_percent_done = round(progress_dict[RIGHT] * 100.0 / progress_dict[TOTAL_FRAMES_KEY])

    if progress_dict[FOUND_OPTIMAL_OFFSET_KEY]:
        optimal_offset_percent_done = 1
    else:
        optimal_offset_percent_done = 0

    percent_done = 0.475 * left_video_percent_done / 100.0 + \
                   0.475 * right_video_percent_done / 100.0 + \
                   0.05 * optimal_offset_percent_done
    percent_done = percent_done * 100.0

    # Message: Frames processed for left video: frames_processed/total_frames (percent%)
    left_video_process_message = "".join([
        "Frames processed for left video: ",
        str(progress_dict[LEFT]),
        "/",
        str(progress_dict[TOTAL_FRAMES_KEY]),
        " (",
        str(left_video_percent_done),
        "%)"
    ])
    right_video_process_message = "".join([
        "Frames processed for right video: ",
        str(progress_dict[RIGHT]),
        "/",
        str(progress_dict[TOTAL_FRAMES_KEY]),
        " (",
        str(right_video_percent_done),
        "%)"
    ])

    if progress_dict[FOUND_OPTIMAL_OFFSET_KEY]:
        finding_optimal_offset_message = "".join(["Found optimal offset! (Left video offset: ",
                                                  str(progress_dict[LEFT_OFFSET_KEY]),
                                                  ", Right video offset: ",
                                                  str(progress_dict[RIGHT_OFFSET_KEY]),
                                                  ")"])
    else:
        finding_optimal_offset_message = "Calculating optimal offset..."

    message_list = [
        left_video_process_message,
        right_video_process_message,
        finding_optimal_offset_message
    ]

    controller.update_frame({PROGRESS_SCREEN_PERCENT_DONE: percent_done, PROGRESS_SCREEN_MESSAGE_LIST: message_list})


def calculate_gradient_gui_version(controller, video_capture_object, start_frame, end_frame_inclusive,
                                   num_frames_to_scan, video_side, progress_dict):
    feed = video_capture_object
    feed.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    prev_frame = cv2.cvtColor(feed.read()[1], cv2.COLOR_BGR2GRAY)
    _, prev_frame = cv2.threshold(prev_frame, 150, 255, cv2.THRESH_TOZERO)
    idx = 0
    gradient = np.empty(num_frames_to_scan - 1)

    while True:
        frame_num = feed.get(cv2.CAP_PROP_POS_FRAMES)

        if frame_num > end_frame_inclusive - 1:
            break

        success, frame = feed.read()
        if not success:
            break

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, frame = cv2.threshold(frame, 150, 255, cv2.THRESH_TOZERO)

        gradient[idx] = np.sum(abs(frame - prev_frame))

        idx += 1

        if idx == 0 or idx % 500 == 0:
            progress_dict[video_side] = idx
            update_ui(progress_dict, controller)

    progress_dict[video_side] = idx
    update_ui(progress_dict, controller)

    return gradient


def main():
    parser = argparse.ArgumentParser(description='Frame match two videos')
    parser.add_argument('left_feed', type=str, help='file name of left feed')
    parser.add_argument('right_feed', type=str, help='file name of right feed')
    parser.add_argument('--start_timestamp', type=int, help='timestamp of clip beginning in seconds')
    parser.add_argument('--end_timestamp', type=int, help='timestamp of clip end in seconds')

    args = parser.parse_args()

    l_offset, r_offset, l_gradient, r_gradient = frame_match(args.left_feed, args.right_feed, args.start_timestamp,
                                                             args.end_timestamp)

    plot_intensity_curves(l_gradient, r_gradient)
    compare_feeds(sys.argv[1], sys.argv[2], l_gradient, l_offset, r_offset)


if __name__ == '__main__':
    main()
