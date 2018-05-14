from tkinter import *
from gui.gui_base_frame import GuiBaseFrame
from gui.pipeline1.utilities.inputs import setup_hms_input
from gui.widgets.header1_label import Header1Label
from gui.widgets.p_label import PLabel


class SrFrameSuggestionTimeStartScreen(GuiBaseFrame):
    def __init__(self, parent, controller, **kw):
        GuiBaseFrame.__init__(self, parent, controller, **kw)

    def setup_widgets(self):
        self.content_wrapper = Frame(self)
        self.content_wrapper.configure(bg="white")

        self.screen_title = Header1Label(self.content_wrapper,
                                         text="Chessboard Frame Suggestion")
        self.screen_instruction_1_label = PLabel(self.content_wrapper)
        self.screen_instruction_2_label = PLabel(self.content_wrapper,
                                                 text="What was the time stamp when this happened?")

        self.input_content_wrapper = Frame(self.content_wrapper)
        setup_hms_input(self, self.input_content_wrapper)

        self.next_button = Button(self.content_wrapper, text="Next",
                                  command=lambda: self.controller.show_next_frame())

        self.screen_title.pack()
        self.screen_instruction_1_label.pack()
        self.screen_instruction_2_label.pack()
        self.input_content_wrapper.pack()
        self.next_button.pack()
        self.content_wrapper.place(relx=0.5, rely=0.45, anchor=CENTER)

    def start(self):
        self.screen_instruction_1_label.configure(text="Please open the following video and\n"
                                                       "find the first frame where a chessboard appears.\n\n" +
                                                       self.controller.get_filename_of_video_with_0_offset() +
                                                       "\n")

    def update_frame(self, data):
        pass

    def stop(self):
        pass
