import datetime
from tkinter import *
from gui.gui_base_frame import GuiBaseFrame
from gui.pipeline1.sr_frame_suggestion_time_start_screen import SrFrameSuggestionTimeStartScreen
from gui.pipeline1.utilities.inputs import setup_hms_input, calculate_frame_num_from_inputs, create_error_message_string
from gui.widgets.header1_label import Header1Label
from gui.widgets.p_label import PLabel

ENTRY_WIDTH = 5


class SrFrameSuggestionTimeEndScreen(GuiBaseFrame):
    def __init__(self, parent, controller, **kw):
        GuiBaseFrame.__init__(self, parent, controller, **kw)

    def setup_widgets(self):
        self.content_wrapper = Frame(self)
        self.content_wrapper.configure(bg="white")

        self.screen_title = Header1Label(self.content_wrapper,
                                         text="Chessboard Frame Suggestion")
        self.screen_instruction_label = PLabel(self.content_wrapper,
                                               text="What was the time stamp when the chessboard went out of view?")
        self.input_content_wrapper = Frame(self.content_wrapper)
        self.hour_input, self.minute_input, self.seconds_input = setup_hms_input(self, self.input_content_wrapper)
        self.error_message_label = PLabel(self.content_wrapper)
        self.screen_navigation_button_wrapper = Frame(self.content_wrapper)
        self.back_button = Button(self.screen_navigation_button_wrapper, text="Back",
                                  command=lambda: self.controller.show_frame(SrFrameSuggestionTimeStartScreen))
        self.next_button = Button(self.screen_navigation_button_wrapper, text="Next",
                                  command=lambda: self.next_button_command())

        self.screen_title.pack()
        self.screen_instruction_label.pack()
        self.input_content_wrapper.pack()
        self.error_message_label.pack()
        self.back_button.grid(row=0, column=0)
        self.next_button.grid(row=0, column=1)
        self.screen_navigation_button_wrapper.pack()
        self.content_wrapper.place(relx=0.5, rely=0.45, anchor=CENTER)

    def start(self):
        self.error_message_label.configure(text="")

    def update_frame(self, data):
        pass

    def stop(self):
        pass

    def next_button_command(self):
        frame_num_inputted = calculate_frame_num_from_inputs(self.hour_input, self.minute_input, self.seconds_input)
        seconds = frame_num_inputted / 30
        left_frame_num = frame_num_inputted + self.controller.video_offsets.left_offset
        right_frame_num = frame_num_inputted + self.controller.video_offsets.right_offset

        if not self.controller.is_frame_num_valid(frame_num_inputted):
            create_error_message_string(self.error_message_label, seconds, frame_num_inputted,
                                        self.controller.video_offsets.left_offset, left_frame_num,
                                        self.controller.video_frame_loader.last_frame_num_left,
                                        self.controller.video_offsets.right_offset,
                                        right_frame_num,
                                        self.controller.video_frame_loader.last_frame_num_right)
        elif seconds < self.controller.sr_scan_start_seconds:
            error_message_string = "".join([
                "The provided timestamp must be greater than or equal to the provided timestamp earlier.\n",
                "Timestamp provided earlier: ",
                str(datetime.timedelta(seconds=self.controller.sr_scan_start_seconds)),
                "\nTimestamp provided here: ",
                str(datetime.timedelta(seconds=seconds))
            ])
            self.error_message_label.configure(text=error_message_string, fg="red")
        else:
            self.error_message_label.configure(text="")
            self.controller.show_next_frame()
