from gui.pipeline1.constants import APPLY_SR_SCREEN_TITLE
from gui.pipeline1.utilities.inputs import calculate_frame_num_from_inputs, create_error_message_string
from gui.pipeline1.utilities.time_selection_start_screen import TimeSelectionStartScreen


class ApplySrTimeStartScreen(TimeSelectionStartScreen):
    def __init__(self, parent, controller, **kw):
        TimeSelectionStartScreen.__init__(self, parent, controller, **kw)

    def init_widgets(self):
        super(ApplySrTimeStartScreen, self).init_widgets()

    def add_widgets_to_frame(self):
        super(ApplySrTimeStartScreen, self).add_widgets_to_frame()

    def on_show_frame(self):
        self.screen_title.configure(text=APPLY_SR_SCREEN_TITLE)
        self.screen_instruction_1_label.configure(text="Please open the following video and\n"
                                                       "find the timestamp where the video should start.\n")
        self.screen_instruction_1_filename_label.configure(text=self.controller.get_filename_of_video_with_0_offset()
                                                                + "\n")
        self.screen_instruction_2_label.configure(text="What was the timestamp?")
        self.error_message_label.configure(text="")

    def update_frame(self, data):
        super(ApplySrTimeStartScreen, self).update_frame(data)

    def on_hide_frame(self):
        self.controller.apply_sr_frame_range.first_frame = calculate_frame_num_from_inputs(self)

    # def set_input_checks(self):


    def next_button_command(self):
        frame_num_inputted = calculate_frame_num_from_inputs(self)
        seconds = frame_num_inputted / 30
        left_frame_num = frame_num_inputted + self.controller.video_offsets.left_offset
        right_frame_num = frame_num_inputted + self.controller.video_offsets.right_offset

        if not self.controller.is_frame_num_within_video_bounds(frame_num_inputted):
            error_string = create_error_message_string(frame_num_inputted,
                                                       self.controller.video_offsets.left_offset, left_frame_num,
                                                       self.controller.video_frame_loader.last_frame_num_left,
                                                       self.controller.video_offsets.right_offset,
                                                       right_frame_num,
                                                       self.controller.video_frame_loader.last_frame_num_right)
            self.error_message_label.configure(text=error_string, fg="red")
        else:
            self.controller.apply_sr_start_seconds = seconds
            self.error_message_label.configure(text="")
            self.controller.show_next_frame()
