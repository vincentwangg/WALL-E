from tkinter import *
from gui.gui_base_frame import GuiBaseFrame
from gui.pipeline1.constants import VIDEO_HEIGHT, VIDEO_WIDTH
from gui.widgets.header1_label import Header1Label
from gui.widgets.p_label import PLabel

TITLE_ROW = 0
SUBTITLE_ROW = TITLE_ROW + 1
FRAME_NUM_ROW = SUBTITLE_ROW + 1
VIDEO_FRAMES_ROW = FRAME_NUM_ROW + 1
OFFSET_INC_INSTR_ROW = VIDEO_FRAMES_ROW + 1
OFFSET_INC_BUTTONS = OFFSET_INC_INSTR_ROW + 1
VIDEO_NAVIGATION_ROW = OFFSET_INC_BUTTONS + 1
VIDEO_BUTTONS_ROW_1 = VIDEO_NAVIGATION_ROW + 1
VIDEO_BUTTONS_ROW_2 = VIDEO_BUTTONS_ROW_1 + 1
NEXT_BUTTON_ROW = VIDEO_BUTTONS_ROW_2 + 1

LEFT_FRAME_NUM_PREFIX = "Left Video Frame: "
RIGHT_FRAME_NUM_PREFIX = "Right Video Frame: "

LEFT_OFFSET_PREFIX = "Left Offset: "
RIGHT_OFFSET_PREFIX = "Right Offset: "


class VideoFramePlayer(GuiBaseFrame):
    def __init__(self, parent, controller, **kw):
        GuiBaseFrame.__init__(self, parent, controller, **kw)
        self.left_video_filename = None
        self.right_video_filename = None
        self.video_frame_loader = None

        self.frame_num = 0

    def setup_widgets(self):
        self.buttons = []
        self.content_wrapper = Frame(self)

        self.title_label = Header1Label(self.content_wrapper, text="Frame Offset Validation")
        self.subtitle_label = PLabel(self.content_wrapper,
                                     text="Use the buttons below to ensure that the video frame offset is valid.")
        self.title_label.grid(row=TITLE_ROW, column=0, columnspan=12)
        self.subtitle_label.grid(row=SUBTITLE_ROW, column=0, columnspan=12)

        self.left_frame_num_label = PLabel(self.content_wrapper)
        self.right_frame_num_label = PLabel(self.content_wrapper)
        self.left_frame_num_label.grid(row=FRAME_NUM_ROW, column=0, columnspan=6)
        self.right_frame_num_label.grid(row=FRAME_NUM_ROW, column=6, columnspan=6)

        self.left_video_label = PLabel(self.content_wrapper)
        self.right_video_label = PLabel(self.content_wrapper)
        self.left_video_label.grid(row=VIDEO_FRAMES_ROW, column=0, columnspan=6)
        self.right_video_label.grid(row=VIDEO_FRAMES_ROW, column=6, columnspan=6)

        self.left_offset_label = PLabel(self.content_wrapper)
        self.right_offset_label = PLabel(self.content_wrapper)
        self.left_offset_label.grid(row=OFFSET_INC_INSTR_ROW, column=0, columnspan=2)
        self.right_offset_label.grid(row=OFFSET_INC_INSTR_ROW, column=10, columnspan=2)

        self.left_offset_inc_instr = PLabel(self.content_wrapper, text="Increase left video offset by:")
        self.right_offset_inc_instr = PLabel(self.content_wrapper, text="Increase right video offset by:")
        self.left_offset_inc_instr.grid(row=OFFSET_INC_INSTR_ROW, column=3, columnspan=3)
        self.right_offset_inc_instr.grid(row=OFFSET_INC_INSTR_ROW, column=6, columnspan=3)

        self.left_offset_inc_10_button = Button(self.content_wrapper, text="+10",
                                                command=lambda: self.adjust_left_offset(10))
        self.left_offset_inc_5_button = Button(self.content_wrapper, text="+5",
                                               command=lambda: self.adjust_left_offset(5))
        self.left_offset_inc_1_button = Button(self.content_wrapper, text="+1",
                                               command=lambda: self.adjust_left_offset(1))
        self.right_offset_inc_1_button = Button(self.content_wrapper, text="+1",
                                                command=lambda: self.adjust_right_offset(1))
        self.right_offset_inc_5_button = Button(self.content_wrapper, text="+5",
                                                command=lambda: self.adjust_right_offset(5))
        self.right_offset_inc_10_button = Button(self.content_wrapper, text="+10",
                                                 command=lambda: self.adjust_right_offset(10))
        self.left_offset_inc_10_button.grid(row=OFFSET_INC_BUTTONS, column=3)
        self.left_offset_inc_5_button.grid(row=OFFSET_INC_BUTTONS, column=4)
        self.left_offset_inc_1_button.grid(row=OFFSET_INC_BUTTONS, column=5)
        self.right_offset_inc_1_button.grid(row=OFFSET_INC_BUTTONS, column=6)
        self.right_offset_inc_5_button.grid(row=OFFSET_INC_BUTTONS, column=7)
        self.right_offset_inc_10_button.grid(row=OFFSET_INC_BUTTONS, column=8)
        self.buttons.extend([self.left_offset_inc_10_button, self.left_offset_inc_5_button,
                             self.left_offset_inc_1_button, self.right_offset_inc_1_button,
                             self.right_offset_inc_5_button, self.right_offset_inc_10_button])

        self.video_navigation_label = PLabel(self.content_wrapper, text="Video navigation:")
        self.video_navigation_label.grid(row=VIDEO_NAVIGATION_ROW, column=0, columnspan=12)

        self.left_video_frame_inc_10_button = Button(self.content_wrapper, text="-10",
                                                     command=lambda: self.adjust_frame_num(-10))
        self.left_video_frame_inc_5_button = Button(self.content_wrapper, text="-5",
                                                    command=lambda: self.adjust_frame_num(-5))
        self.left_video_frame_inc_1_button = Button(self.content_wrapper, text="-1",
                                                    command=lambda: self.adjust_frame_num(-1))
        self.right_video_frame_inc_1_button = Button(self.content_wrapper, text="+1",
                                                     command=lambda: self.adjust_frame_num(1))
        self.right_video_frame_inc_5_button = Button(self.content_wrapper, text="+5",
                                                     command=lambda: self.adjust_frame_num(5))
        self.right_video_frame_inc_10_button = Button(self.content_wrapper, text="+10",
                                                      command=lambda: self.adjust_frame_num(10))
        self.left_video_frame_inc_10_button.grid(row=VIDEO_BUTTONS_ROW_1, column=3)
        self.left_video_frame_inc_5_button.grid(row=VIDEO_BUTTONS_ROW_1, column=4)
        self.left_video_frame_inc_1_button.grid(row=VIDEO_BUTTONS_ROW_1, column=5)
        self.right_video_frame_inc_1_button.grid(row=VIDEO_BUTTONS_ROW_1, column=6)
        self.right_video_frame_inc_5_button.grid(row=VIDEO_BUTTONS_ROW_1, column=7)
        self.right_video_frame_inc_10_button.grid(row=VIDEO_BUTTONS_ROW_1, column=8)
        self.buttons.extend([self.left_video_frame_inc_10_button, self.left_video_frame_inc_5_button,
                             self.left_video_frame_inc_1_button, self.right_video_frame_inc_1_button,
                             self.right_video_frame_inc_5_button, self.right_video_frame_inc_10_button])

        self.left_video_frame_inc_300_button = Button(self.content_wrapper, text="-300",
                                                      command=lambda: self.adjust_frame_num(-300))
        self.left_video_frame_inc_150_button = Button(self.content_wrapper, text="-150",
                                                      command=lambda: self.adjust_frame_num(-150))
        self.left_video_frame_inc_30_button = Button(self.content_wrapper, text="-30",
                                                     command=lambda: self.adjust_frame_num(-30))
        self.right_video_frame_inc_30_button = Button(self.content_wrapper, text="+30",
                                                      command=lambda: self.adjust_frame_num(30))
        self.right_video_frame_inc_150_button = Button(self.content_wrapper, text="+150",
                                                       command=lambda: self.adjust_frame_num(150))
        self.right_video_frame_inc_300_button = Button(self.content_wrapper, text="+300",
                                                       command=lambda: self.adjust_frame_num(300))
        self.left_video_frame_inc_300_button.grid(row=VIDEO_BUTTONS_ROW_2, column=3)
        self.left_video_frame_inc_150_button.grid(row=VIDEO_BUTTONS_ROW_2, column=4)
        self.left_video_frame_inc_30_button.grid(row=VIDEO_BUTTONS_ROW_2, column=5)
        self.right_video_frame_inc_30_button.grid(row=VIDEO_BUTTONS_ROW_2, column=6)
        self.right_video_frame_inc_150_button.grid(row=VIDEO_BUTTONS_ROW_2, column=7)
        self.right_video_frame_inc_300_button.grid(row=VIDEO_BUTTONS_ROW_2, column=8)
        self.buttons.extend([self.left_video_frame_inc_300_button, self.left_video_frame_inc_150_button,
                             self.left_video_frame_inc_30_button, self.right_video_frame_inc_30_button,
                             self.right_video_frame_inc_150_button, self.right_video_frame_inc_300_button])

        self.next_button = Button(self.content_wrapper, text="Next")
        self.next_button.grid(row=NEXT_BUTTON_ROW, column=0, columnspan=12)

        self.content_wrapper.pack()

    def set_video_frame(self, frame_num, left_offset, right_offset):
        _, left_img = \
            self.controller.video_frame_loader.get_left_frame_tkinter_with_resize(frame_num + left_offset,
                                                                                  VIDEO_WIDTH, VIDEO_HEIGHT)
        _, right_img = \
            self.controller.video_frame_loader.get_right_frame_tkinter_with_resize(frame_num + right_offset,
                                                                                   VIDEO_WIDTH, VIDEO_HEIGHT)

        self.left_video_label.configure(image=left_img)
        self.left_video_label.image = left_img

        self.right_video_label.configure(image=right_img)
        self.right_video_label.image = right_img

    def start(self):
        self.update_UI()

    def update_frame(self, data):
        pass

    def stop(self):
        # TODO
        pass

    def update_UI(self):
        self.ensure_frame_num_is_valid()

        self.set_video_frame(self.frame_num, self.controller.video_offsets.left_offset,
                             self.controller.video_offsets.right_offset)
        self.left_frame_num_label.configure(text=LEFT_FRAME_NUM_PREFIX +
                                                 str(self.frame_num + self.controller.video_offsets.left_offset))
        self.right_frame_num_label.configure(text=RIGHT_FRAME_NUM_PREFIX +
                                                  str(self.frame_num + self.controller.video_offsets.right_offset))
        self.left_offset_label.configure(text=LEFT_OFFSET_PREFIX + str(self.controller.video_offsets.left_offset))
        self.right_offset_label.configure(text=RIGHT_OFFSET_PREFIX + str(self.controller.video_offsets.right_offset))

    def ensure_frame_num_is_valid(self):
        if self.frame_num < 0:
            self.frame_num = 0

        left_offset = self.controller.video_offsets.left_offset
        right_offset = self.controller.video_offsets.right_offset
        last_frame_left = self.controller.video_frame_loader.frame_count_left
        last_frame_right = self.controller.video_frame_loader.frame_count_right

        if self.frame_num + left_offset > last_frame_left:
            self.frame_num = last_frame_left - left_offset
        if self.frame_num + right_offset > last_frame_right:
            self.frame_num = last_frame_left - right_offset

    def adjust_frame_num(self, value):
        self.frame_num += value
        self.update_UI()

    def adjust_left_offset(self, value):
        self.controller.video_offsets.left_offset += value
        self.normalize_offsets()
        self.update_UI()

    def adjust_right_offset(self, value):
        self.controller.video_offsets.right_offset += value
        self.normalize_offsets()
        self.update_UI()

    def normalize_offsets(self):
        if self.controller.video_offsets.left_offset > self.controller.video_offsets.right_offset:
            self.controller.video_offsets.left_offset -= self.controller.video_offsets.right_offset
            self.controller.video_offsets.right_offset = 0
        elif self.controller.video_offsets.left_offset < self.controller.video_offsets.right_offset:
            self.controller.video_offsets.right_offset -= self.controller.video_offsets.left_offset
            self.controller.video_offsets.left_offset = 0
        else:
            self.controller.video_offsets.left_offset = 0
            self.controller.video_offsets.right_offset = 0
