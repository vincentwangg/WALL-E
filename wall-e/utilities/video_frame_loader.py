import cv2
from gui.pipeline1.video_scan_screen import COUNTING_LEFT_FRAMES_MESSAGE, COUNTING_RIGHT_FRAMES_MESSAGE, \
    LEFT_FRAMES_COUNT_PREFIX, RIGHT_FRAMES_COUNT_PREFIX


class VideoFrameLoader:
    def __init__(self, left_feed_filename, right_feed_filename):
        self.vc_left = cv2.VideoCapture(left_feed_filename)
        self.vc_right = cv2.VideoCapture(right_feed_filename)
        self.frame_count_left = None
        self.frame_count_right = None

    def get_left_frame(self, frame_num):
        self.vc_left.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        return self.vc_left.read()

    def get_right_frame(self, frame_num):
        self.vc_right.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        return self.vc_right.read()

    def get_next_left_frame(self):
        return self.vc_left.read()

    def get_next_right_frame(self):
        return self.vc_right.read()

    def count_frames_in_videos(self, controller):
        if self.frame_count_left is None:
            controller.update_frame(COUNTING_LEFT_FRAMES_MESSAGE)
            self.frame_count_left = count_frames_in_vc_object(self.vc_left, controller, LEFT_FRAMES_COUNT_PREFIX)

        if self.frame_count_right is None:
            controller.update_frame(COUNTING_RIGHT_FRAMES_MESSAGE)
            self.frame_count_right = count_frames_in_vc_object(self.vc_right, controller, RIGHT_FRAMES_COUNT_PREFIX)

        return self.frame_count_left, self.frame_count_right


def count_frames_in_vc_object(vc_obj, controller, message_prefix):
    vc_obj.set(cv2.CAP_PROP_POS_FRAMES, 0)

    count = 0
    while True:
        success, _ = vc_obj.read()

        if not success:
            break

        count += 1

        # Update the controller every 100 frames
        if count == 0 or count % 1000 == 0:
            controller.update_frame(message_prefix + str(count))

    controller.update_frame(message_prefix + str(count))
    return count
