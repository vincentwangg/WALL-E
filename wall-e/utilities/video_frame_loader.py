import cv2


class VideoFrameLoader:
    def __init__(self, left_feed_filename, right_feed_filename):
        self.vc_left = cv2.VideoCapture(left_feed_filename)
        self.vc_right = cv2.VideoCapture(right_feed_filename)

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
