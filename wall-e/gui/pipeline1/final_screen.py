from Tkinter import Frame, Button, CENTER

import sys

from gui.pipeline1.utilities.constants import SCREENS_REL_X, SCREEN_REL_Y_45
from gui.widgets.gui_base_frame import GuiBaseFrame
from gui.widgets.header1_label import Header1Label
from gui.widgets.p_label import PLabel


class FinalScreen(GuiBaseFrame):
    def __init__(self, parent, controller, **kw):
        GuiBaseFrame.__init__(self, parent, controller, **kw)

    def init_widgets(self):
        self.text_container = Frame(self)
        self.screen_title = Header1Label(self.text_container,
                                         text="Stereo Rectification Complete!")
        self.text_1 = PLabel(self.text_container, text=("\n".join(["Your videos have been stereo rectified!",
                                                                   "You can find them in the follow "
                                                                   "paths on your system:"])))
        self.filenames = PLabel(self.text_container)
        self.thanks_label = PLabel(self.text_container, text="Thank you for your patience!")
        self.finish_button = Button(self.text_container, text="Finish and Close Window",
                                    command=lambda: sys.exit())

    def add_widgets_to_frame(self):
        self.screen_title.pack()
        self.text_1.pack()
        self.filenames.pack()
        self.thanks_label.pack()
        self.finish_button.pack()
        self.text_container.place(relx=SCREENS_REL_X, rely=SCREEN_REL_Y_45, anchor=CENTER)

    def on_show_frame(self):
        self.filenames.configure(text=("\n".join([
            "Left video:", self.controller.left_video_filename_sr,
            "",
            "Right video:", self.controller.right_video_filename_sr
        ])))

    def on_hide_frame(self):
        pass
