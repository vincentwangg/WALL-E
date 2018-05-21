from gui.pipeline1.constants import SR_FRAME_SELECTION_TITLE
from gui.pipeline1.utilities.inputs import calculate_frame_num_from_inputs, create_error_message_string
from gui.pipeline1.utilities.time_start_selection_screen import TimeStartScreen
from gui.widgets.gui_base_frame import GuiBaseFrame


class SrFrameSuggestionTimeStartScreen(TimeStartScreen):
    def __init__(self, parent, controller, **kw):
        GuiBaseFrame.__init__(self, parent, controller, **kw)

    def start(self):
        self.screen_title.configure(text=SR_FRAME_SELECTION_TITLE)
        self.screen_instruction_1_label.configure(text="Please open the following video and\n"
                                                       "find the first timestamp where a chessboard appears.\n")
        self.screen_instruction_1_filename_label.configure(text=self.controller.get_filename_of_video_with_0_offset()
                                                                + "\n")
        self.screen_instruction_2_label.configure(text="What was the timestamp when this happened?")
        self.error_message_label.configure(text="")

    def update_frame(self, data):
        pass

    def stop(self):
        self.controller.sr_scan_range.first_frame = calculate_frame_num_from_inputs(self.hour_input,
                                                                                    self.minute_input,
                                                                                    self.seconds_input)

    def next_button_command(self):
        frame_num_inputted = calculate_frame_num_from_inputs(self.hour_input, self.minute_input, self.seconds_input)
        seconds = frame_num_inputted / 30
        left_frame_num = frame_num_inputted + self.controller.video_offsets.left_offset
        right_frame_num = frame_num_inputted + self.controller.video_offsets.right_offset

        if not self.controller.is_frame_num_valid(frame_num_inputted):
            error_string = create_error_message_string(seconds, frame_num_inputted,
                                                       self.controller.video_offsets.left_offset, left_frame_num,
                                                       self.controller.video_frame_loader.last_frame_num_left,
                                                       self.controller.video_offsets.right_offset,
                                                       right_frame_num,
                                                       self.controller.video_frame_loader.last_frame_num_right)
            self.error_message_label.configure(text=error_string, fg="red")
        else:
            self.controller.sr_scan_start_seconds = seconds
            self.error_message_label.configure(text="")
            self.controller.show_next_frame()
