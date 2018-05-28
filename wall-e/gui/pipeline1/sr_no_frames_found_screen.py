from Tkinter import Frame, LEFT, Button, CENTER

from gui.pipeline1.sr_frame_suggestion_intro_screen import SrFrameSuggestionIntroScreen
from gui.pipeline1.utilities.constants import SCREENS_REL_X, SCREEN_REL_Y_45, SR_FRAME_SELECTION_TITLE
from gui.widgets.gui_base_frame import GuiBaseFrame
from gui.widgets.header1_label import Header1Label
from gui.widgets.p_label import PLabel


class SrNoFramesFoundScreen(GuiBaseFrame):
    def __init__(self, parent, controller, **kw):
        GuiBaseFrame.__init__(self, parent, controller, **kw)

    def init_widgets(self):
        self.text_container = Frame(self)
        self.screen_title = Header1Label(self.text_container, text=SR_FRAME_SELECTION_TITLE)
        self.description_label = PLabel(self.text_container,
                                        text="\n\n".join([
                                            "There were no frames found that were\n"
                                            "valid for stereo rectification. :(",
                                            "Please try again with a time range that has\n"
                                            "a better view of the full chessboard."
                                        ]))
        self.empty_space = PLabel(self.text_container)
        self.next_button = Button(self.text_container, text="Try Again",
                                  command=lambda: self.controller.show_frame(SrFrameSuggestionIntroScreen))

    def add_widgets_to_frame(self):
        self.screen_title.pack()
        self.description_label.pack()
        self.empty_space.pack()
        self.next_button.pack()
        self.text_container.place(relx=SCREENS_REL_X, rely=SCREEN_REL_Y_45, anchor=CENTER)

    def on_show_frame(self):
        pass

    def on_hide_frame(self):
        pass
