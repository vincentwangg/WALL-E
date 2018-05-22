from tkinter import *

from gui.pipeline1.constants import SCREENS_REL_X, SCREENS_REL_Y, APPLY_SR_SCREEN_TITLE
from gui.widgets.gui_base_frame import GuiBaseFrame
from gui.widgets.header1_label import Header1Label
from gui.widgets.p_label import PLabel


class ApplySrIntroScreen(GuiBaseFrame):
    def __init__(self, parent, controller, **kw):
        GuiBaseFrame.__init__(self, parent, controller, **kw)

    def init_widgets(self):
        self.content_wrapper = Frame(self)

        self.screen_title = Header1Label(self.content_wrapper, text=APPLY_SR_SCREEN_TITLE)
        self.screen_description_label = PLabel(self.content_wrapper,
                                               text="\nFor long videos, it may take hours to create\na new stereo "
                                                    "rectified video.\n\nIn the next few screens, you may enter "
                                                    "timestamps to\ncrop the video to save time on\ncreating the "
                                                    "stereo rectified footage.\n\nIf you feel that this step isn't "
                                                    "necessary,\nfeel free to press skip.\n")
        self.button_wrapper = Frame(self.content_wrapper)
        self.next_button = Button(self.button_wrapper, text="Next",
                                  command=lambda: self.controller.show_next_frame())
        self.skip_button = Button(self.button_wrapper, text="Skip",
                                  command=lambda: self.skip_sr_frame_suggestion())

    def add_widgets_to_frame(self):
        self.screen_title.pack()
        self.screen_description_label.pack()
        self.button_wrapper.pack()
        self.next_button.grid(row=0, column=0)
        self.skip_button.grid(row=0, column=1)
        self.content_wrapper.place(relx=SCREENS_REL_X, rely=SCREENS_REL_Y, anchor=CENTER)

    def on_show_frame(self):
        pass

    def update_frame(self, data):
        pass

    def on_hide_frame(self):
        pass

    def skip_sr_frame_suggestion(self):
        self.controller.sr_scan_frame_range.reset_to_default()
        # self.controller.show_frame()
