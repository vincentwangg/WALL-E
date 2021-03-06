from Tkinter import Frame, Button, CENTER

from gui.pipeline1.utilities.constants import VIDEO_PREVIEW_HEIGHT, VIDEO_PREVIEW_WIDTH, SCREENS_REL_X, \
    SCREEN_REL_Y_50
from gui.widgets.gui_base_frame import GuiBaseFrame
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

SLOW_FORWARD_PREFIX = "> "
NORMAL_FORWARD_PREFIX = ">> "
FAST_FORWARD_PREFIX = ">>> "

SLOW_BACK_PREFIX = "< "
NORMAL_BACK_PREFIX = "<< "
FAST_BACK_PREFIX = "<<< "

FORWARD_1_FRAME_TEXT = SLOW_FORWARD_PREFIX + "1 (1/30 second)"
FORWARD_5_FRAMES_TEXT = SLOW_FORWARD_PREFIX + "5 (1/6 second)"
FORWARD_10_FRAMES_TEXT = SLOW_FORWARD_PREFIX + "10 (1/3 second)"
FORWARD_30_FRAMES_TEXT = NORMAL_FORWARD_PREFIX + "30 (1 second)"
FORWARD_150_FRAMES_TEXT = FAST_FORWARD_PREFIX + "150 (5 seconds)"
FORWARD_300_FRAMES_TEXT = FAST_FORWARD_PREFIX + "300 (10 seconds)"

BACK_1_FRAME_TEXT = SLOW_BACK_PREFIX + "1 (1/30 second)"
BACK_5_FRAMEs_TEXT = SLOW_BACK_PREFIX + "5 (1/6 second)"
BACK_10_FRAMEs_TEXT = SLOW_BACK_PREFIX + "10 (1/3 second)"
BACK_30_FRAMEs_TEXT = NORMAL_BACK_PREFIX + "30 (1 second)"
BACK_150_FRAMEs_TEXT = FAST_BACK_PREFIX + "150 (5 seconds)"
BACK_300_FRAMEs_TEXT = FAST_BACK_PREFIX + "300 (10 seconds)"

LEFT_VIDEO_FORWARD_1_FRAME_TEXT = FORWARD_1_FRAME_TEXT
LEFT_VIDEO_FORWARD_5_FRAME_TEXT = FORWARD_5_FRAMES_TEXT
LEFT_VIDEO_FORWARD_10_FRAME_TEXT = FORWARD_10_FRAMES_TEXT
LEFT_VIDEO_FORWARD_30_FRAME_TEXT = FORWARD_30_FRAMES_TEXT
LEFT_VIDEO_FORWARD_150_FRAME_TEXT = FORWARD_150_FRAMES_TEXT
LEFT_VIDEO_FORWARD_300_FRAME_TEXT = FORWARD_300_FRAMES_TEXT

RIGHT_VIDEO_FORWARD_1_FRAME_TEXT = FORWARD_1_FRAME_TEXT
RIGHT_VIDEO_FORWARD_5_FRAME_TEXT = FORWARD_5_FRAMES_TEXT
RIGHT_VIDEO_FORWARD_10_FRAME_TEXT = FORWARD_10_FRAMES_TEXT
RIGHT_VIDEO_FORWARD_30_FRAME_TEXT = FORWARD_30_FRAMES_TEXT
RIGHT_VIDEO_FORWARD_150_FRAME_TEXT = FORWARD_150_FRAMES_TEXT
RIGHT_VIDEO_FORWARD_300_FRAME_TEXT = FORWARD_300_FRAMES_TEXT


class FrameMatchingValidationScreen(GuiBaseFrame):
    def __init__(self, parent, controller, **kw):
        GuiBaseFrame.__init__(self, parent, controller, **kw)
        self.left_video_filename = None
        self.right_video_filename = None
        self.video_frame_loader = None

        self.frame_num = 0

    def init_widgets(self):
        self.buttons = []
        self.content_wrapper = Frame(self)

        self.title_label = Header1Label(self.content_wrapper, text="Frame Offset Validation")
        self.subtitle_label = PLabel(self.content_wrapper,
                                     text="Use the buttons below to ensure that the video frame offset is valid. Press Next when finished.")

        self.left_frame_num_label = PLabel(self.content_wrapper)
        self.right_frame_num_label = PLabel(self.content_wrapper)

        self.left_video_label = PLabel(self.content_wrapper)
        self.right_video_label = PLabel(self.content_wrapper)

        self.left_offset_label = PLabel(self.content_wrapper)
        self.right_offset_label = PLabel(self.content_wrapper)

        self.left_offset_inc_instr = PLabel(self.content_wrapper, text="Increase left video offset by:")
        self.right_offset_inc_instr = PLabel(self.content_wrapper, text="Increase right video offset by:")

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
        self.buttons.extend([self.left_offset_inc_10_button, self.left_offset_inc_5_button,
                             self.left_offset_inc_1_button, self.right_offset_inc_1_button,
                             self.right_offset_inc_5_button, self.right_offset_inc_10_button])

        self.video_navigation_label = PLabel(self.content_wrapper, text="Video frame navigation:")

        self.left_video_frame_inc_10_button = Button(self.content_wrapper, text=BACK_10_FRAMEs_TEXT,
                                                     command=lambda: self.adjust_frame_num(-10))
        self.left_video_frame_inc_5_button = Button(self.content_wrapper, text=BACK_5_FRAMEs_TEXT,
                                                    command=lambda: self.adjust_frame_num(-5))
        self.left_video_frame_inc_1_button = Button(self.content_wrapper, text=BACK_1_FRAME_TEXT,
                                                    command=lambda: self.adjust_frame_num(-1))
        self.right_video_frame_inc_1_button = Button(self.content_wrapper, text=FORWARD_1_FRAME_TEXT,
                                                     command=lambda: self.adjust_frame_num(1))
        self.right_video_frame_inc_5_button = Button(self.content_wrapper, text=FORWARD_5_FRAMES_TEXT,
                                                     command=lambda: self.adjust_frame_num(5))
        self.right_video_frame_inc_10_button = Button(self.content_wrapper, text=FORWARD_10_FRAMES_TEXT,
                                                      command=lambda: self.adjust_frame_num(10))
        self.buttons.extend([self.left_video_frame_inc_10_button, self.left_video_frame_inc_5_button,
                             self.left_video_frame_inc_1_button, self.right_video_frame_inc_1_button,
                             self.right_video_frame_inc_5_button, self.right_video_frame_inc_10_button])

        self.left_video_frame_inc_300_button = Button(self.content_wrapper, text=BACK_300_FRAMEs_TEXT,
                                                      command=lambda: self.adjust_frame_num(-300))
        self.left_video_frame_inc_150_button = Button(self.content_wrapper, text=BACK_150_FRAMEs_TEXT,
                                                      command=lambda: self.adjust_frame_num(-150))
        self.left_video_frame_inc_30_button = Button(self.content_wrapper, text=BACK_30_FRAMEs_TEXT,
                                                     command=lambda: self.adjust_frame_num(-30))
        self.right_video_frame_inc_30_button = Button(self.content_wrapper, text=FORWARD_30_FRAMES_TEXT,
                                                      command=lambda: self.adjust_frame_num(30))
        self.right_video_frame_inc_150_button = Button(self.content_wrapper, text=FORWARD_150_FRAMES_TEXT,
                                                       command=lambda: self.adjust_frame_num(150))
        self.right_video_frame_inc_300_button = Button(self.content_wrapper, text=FORWARD_300_FRAMES_TEXT,
                                                       command=lambda: self.adjust_frame_num(300))
        self.buttons.extend([self.left_video_frame_inc_300_button, self.left_video_frame_inc_150_button,
                             self.left_video_frame_inc_30_button, self.right_video_frame_inc_30_button,
                             self.right_video_frame_inc_150_button, self.right_video_frame_inc_300_button])

        self.next_button = Button(self.content_wrapper, text="Next",
                                  command=lambda: self.controller.show_next_frame())

    def add_widgets_to_frame(self):
        self.title_label.grid(row=TITLE_ROW, column=0, columnspan=12)
        self.subtitle_label.grid(row=SUBTITLE_ROW, column=0, columnspan=12)

        self.left_frame_num_label.grid(row=FRAME_NUM_ROW, column=0, columnspan=6)
        self.right_frame_num_label.grid(row=FRAME_NUM_ROW, column=6, columnspan=6)

        self.left_video_label.grid(row=VIDEO_FRAMES_ROW, column=0, columnspan=6)
        self.right_video_label.grid(row=VIDEO_FRAMES_ROW, column=6, columnspan=6)

        self.left_offset_label.grid(row=OFFSET_INC_INSTR_ROW, column=0, columnspan=2)
        self.right_offset_label.grid(row=OFFSET_INC_INSTR_ROW, column=10, columnspan=2)

        self.left_offset_inc_instr.grid(row=OFFSET_INC_INSTR_ROW, column=3, columnspan=3)
        self.right_offset_inc_instr.grid(row=OFFSET_INC_INSTR_ROW, column=6, columnspan=3)

        self.left_offset_inc_10_button.grid(row=OFFSET_INC_BUTTONS, column=3)
        self.left_offset_inc_5_button.grid(row=OFFSET_INC_BUTTONS, column=4)
        self.left_offset_inc_1_button.grid(row=OFFSET_INC_BUTTONS, column=5)
        self.right_offset_inc_1_button.grid(row=OFFSET_INC_BUTTONS, column=6)
        self.right_offset_inc_5_button.grid(row=OFFSET_INC_BUTTONS, column=7)
        self.right_offset_inc_10_button.grid(row=OFFSET_INC_BUTTONS, column=8)

        self.video_navigation_label.grid(row=VIDEO_NAVIGATION_ROW, column=0, columnspan=12)

        self.left_video_frame_inc_10_button.grid(row=VIDEO_BUTTONS_ROW_1, column=0, columnspan=2)
        self.left_video_frame_inc_5_button.grid(row=VIDEO_BUTTONS_ROW_1, column=2, columnspan=2)
        self.left_video_frame_inc_1_button.grid(row=VIDEO_BUTTONS_ROW_1, column=4, columnspan=2)
        self.right_video_frame_inc_1_button.grid(row=VIDEO_BUTTONS_ROW_1, column=6, columnspan=2)
        self.right_video_frame_inc_5_button.grid(row=VIDEO_BUTTONS_ROW_1, column=8, columnspan=2)
        self.right_video_frame_inc_10_button.grid(row=VIDEO_BUTTONS_ROW_1, column=10, columnspan=2)

        self.left_video_frame_inc_300_button.grid(row=VIDEO_BUTTONS_ROW_2, column=0, columnspan=2)
        self.left_video_frame_inc_150_button.grid(row=VIDEO_BUTTONS_ROW_2, column=2, columnspan=2)
        self.left_video_frame_inc_30_button.grid(row=VIDEO_BUTTONS_ROW_2, column=4, columnspan=2)
        self.right_video_frame_inc_30_button.grid(row=VIDEO_BUTTONS_ROW_2, column=6, columnspan=2)
        self.right_video_frame_inc_150_button.grid(row=VIDEO_BUTTONS_ROW_2, column=8, columnspan=2)
        self.right_video_frame_inc_300_button.grid(row=VIDEO_BUTTONS_ROW_2, column=10, columnspan=2)

        self.next_button.grid(row=NEXT_BUTTON_ROW, column=0, columnspan=12)

        self.content_wrapper.place(relx=SCREENS_REL_X, rely=SCREEN_REL_Y_50, anchor=CENTER)


    def set_video_frame(self, frame_num, left_offset, right_offset):
        _, left_img = \
            self.controller.video_frame_loader.get_left_frame_tkinter_with_resize(frame_num + left_offset,
                                                                                  VIDEO_PREVIEW_WIDTH, VIDEO_PREVIEW_HEIGHT)
        _, right_img = \
            self.controller.video_frame_loader.get_right_frame_tkinter_with_resize(frame_num + right_offset,
                                                                                   VIDEO_PREVIEW_WIDTH, VIDEO_PREVIEW_HEIGHT)

        self.left_video_label.configure(image=left_img)
        self.left_video_label.image = left_img

        self.right_video_label.configure(image=right_img)
        self.right_video_label.image = right_img

    def on_show_frame(self):
        self.update_UI()

    def update_frame(self, data):
        pass

    def on_hide_frame(self):
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
        last_frame_left = self.controller.video_frame_loader.last_frame_num_left
        last_frame_right = self.controller.video_frame_loader.last_frame_num_right

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
