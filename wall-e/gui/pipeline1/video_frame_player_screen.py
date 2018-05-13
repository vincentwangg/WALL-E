from tkinter import *
from gui.gui_base_frame import GuiBaseFrame
from gui.pipeline1.constants import VIDEO_HEIGHT, VIDEO_WIDTH
from utilities.image_converter import cv2_image_to_tkinter_with_resize


class VideoFramePlayer(GuiBaseFrame):
    def __init__(self, parent, controller, **kw):
        GuiBaseFrame.__init__(self, parent, controller, **kw)
        self.left_video_filename = None
        self.right_video_filename = None
        self.video_frame_loader = None

        self.left_offset = 0
        self.right_offset = 0

    def setup_widgets(self):
        self.header_label = Label(self, text="Video Frame Player")
        self.left_video_label = Label(self)
        self.right_video_label = Label(self)

        self.header_label.grid(row=0, column=0, columnspan=3, sticky="ew")
        self.left_video_label.grid(row=1, column=0)
        self.right_video_label.grid(row=1, column=1)

    def set_offset_values(self, left_offset=0, right_offset=0):
        self.left_offset = left_offset
        self.right_offset = right_offset

    def set_video_frame(self, frame_num):
        _, left_img = self.controller.video_frame_loader.get_left_frame(frame_num + self.left_offset)
        _, right_img = self.controller.video_frame_loader.get_right_frame(frame_num + self.right_offset)

        left_img = cv2_image_to_tkinter_with_resize(left_img, VIDEO_WIDTH, VIDEO_HEIGHT)
        right_img = cv2_image_to_tkinter_with_resize(right_img, VIDEO_WIDTH, VIDEO_HEIGHT)

        self.left_video_label.configure(image=left_img)
        self.left_video_label.image = left_img

        self.right_video_label.configure(image=right_img)
        self.right_video_label.image = right_img

    def start_video(self):
        # TODO Link frame matching offsets here
        self.set_video_frame(0)

    def start(self):
        # TODO
        pass

    def update_frame(self, data):
        pass

    def stop(self):
        # TODO
        pass
