from tkinter import *

from gui.pipeline1.constants import SCREENS_REL_X, SCREENS_REL_Y, SR_FRAME_SELECTION_TITLE
from gui.pipeline1.sr_scan_screen import SrScanScreen
from gui.widgets.gui_base_frame import GuiBaseFrame
from gui.widgets.header1_label import Header1Label
from gui.widgets.p_label import PLabel


class SrFrameSuggestionIntroScreen(GuiBaseFrame):
    def __init__(self, parent, controller, **kw):
        GuiBaseFrame.__init__(self, parent, controller, **kw)

    def setup_widgets(self):
        self.content_wrapper = Frame(self)

        self.screen_title = Header1Label(self.content_wrapper, text=SR_FRAME_SELECTION_TITLE)
        self.screen_description_label = PLabel(self.content_wrapper,
                                               text="\nFor long videos, it may take hours to search\nfor frames that "
                                                    "contain a chessboard.\n\nAs an option, you can help us save time "
                                                    "by\nchoosing a range of frames that is likely to have\na "
                                                    "chessboard in view.\n\nIf you feel that this step isn't "
                                                    "necessary,\nfeel free to press skip.\n")
        self.button_wrapper = Frame(self.content_wrapper)
        self.next_button = Button(self.button_wrapper, text="Next",
                                  command=lambda: self.controller.show_next_frame())
        self.skip_button = Button(self.button_wrapper, text="Skip",
                                  command=lambda: self.skip_sr_frame_suggestion())

        self.screen_title.pack()
        self.screen_description_label.pack()
        self.button_wrapper.pack()
        self.next_button.grid(row=0, column=0)
        self.skip_button.grid(row=0, column=1)
        self.content_wrapper.place(relx=SCREENS_REL_X, rely=SCREENS_REL_Y, anchor=CENTER)

    def start(self):
        pass

    def update_frame(self, data):
        pass

    def stop(self):
        pass

    def skip_sr_frame_suggestion(self):
        self.controller.sr_scan_range.reset_to_default()
        self.controller.show_frame(SrScanScreen)
