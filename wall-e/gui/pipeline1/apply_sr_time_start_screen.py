from gui.pipeline1.constants import APPLY_SR_SCREEN_TITLE
from gui.pipeline1.utilities.inputs import calculate_frame_num_from_inputs, frame_input_within_video_bounds_check
from gui.pipeline1.utilities.time_selection_start_screen import TimeSelectionStartScreen


class ApplySrTimeStartScreen(TimeSelectionStartScreen):
    def __init__(self, parent, controller, **kw):
        TimeSelectionStartScreen.__init__(self, parent, controller, **kw)

    def init_widgets(self):
        super(ApplySrTimeStartScreen, self).init_widgets()
        self.set_title(APPLY_SR_SCREEN_TITLE)
        self.set_instruction_1_text("Please open the following video and\n"
                                    "find the timestamp where the video should start.\n")
        self.set_instruction_2_text("What was the timestamp?")

    def on_show_frame(self):
        self.set_instruction_1_filename(self.controller.get_filename_of_video_with_0_offset() + "\n")
        self.set_error_message("")

    def on_hide_frame(self):
        self.controller.apply_sr_frame_range.first_frame = calculate_frame_num_from_inputs(self)

    def set_input_checks(self):
        self.add_input_check(lambda screen: frame_input_within_video_bounds_check(self))

    def on_input_check_success(self):
        self.controller.apply_sr_frame_range.first_frame = calculate_frame_num_from_inputs(self)
