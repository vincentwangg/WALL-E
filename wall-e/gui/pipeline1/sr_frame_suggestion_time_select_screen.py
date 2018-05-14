from tkinter import *
from gui.gui_base_frame import GuiBaseFrame
from gui.widgets.header1_label import Header1Label
from gui.widgets.p_label import PLabel

ENTRY_WIDTH = 5


class SrFrameSuggestionTimeSelectScreen(GuiBaseFrame):
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
        self.setup_input()

        self.next_button = Button(self.content_wrapper, text="Next",
                                  command=lambda: self.controller.show_next_frame())

        self.screen_title.pack()
        self.screen_instruction_1_label.pack()
        self.screen_instruction_2_label.pack()
        self.input_content_wrapper.pack()
        self.next_button.pack()
        self.content_wrapper.place(relx=0.5, rely=0.45, anchor=CENTER)

    def setup_input(self):
        self.hour_label = PLabel(self.input_content_wrapper, text="H: ")
        self.hour_input = Entry(self.input_content_wrapper, width=ENTRY_WIDTH, textvariable=IntVar, justify=CENTER)
        self.hour_input.insert(0, 0)
        self.hour_label.grid(row=0, column=0)
        self.hour_input.grid(row=0, column=1)

        self.minute_label = PLabel(self.input_content_wrapper, text="M: ")
        self.minute_input = Entry(self.input_content_wrapper, width=ENTRY_WIDTH, textvariable=IntVar, justify=CENTER)
        self.minute_input.insert(0, 0)
        self.minute_label.grid(row=0, column=2)
        self.minute_input.grid(row=0, column=3)

        self.seconds_label = PLabel(self.input_content_wrapper, text="S: ")
        self.seconds_input = Entry(self.input_content_wrapper, width=ENTRY_WIDTH, textvariable=IntVar, justify=CENTER)
        self.seconds_input.insert(0, 0)
        self.seconds_label.grid(row=0, column=4)
        self.seconds_input.grid(row=0, column=5)

    def start(self):
        self.screen_instruction_1_label.configure(text="Please open the following video and\n"
                                                       "find the first frame where a chessboard appears.\n\n" +
                                                       self.controller.get_filename_of_video_with_0_offset() +
                                                       "\n")

    def update_frame(self, data):
        pass

    def stop(self):
        pass
