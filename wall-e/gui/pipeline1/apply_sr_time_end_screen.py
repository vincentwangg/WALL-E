from gui.pipeline1.constants import APPLY_SR_SCREEN_TITLE
from gui.pipeline1.utilities.inputs import frame_input_within_video_bounds_check, sr_scan_frame_range_valid_check, \
    calculate_frame_num_from_inputs, apply_sr_frame_range_valid_check
from gui.pipeline1.utilities.time_selection_end_screen import TimeSelectionEndScreen


class ApplySrTimeEndScreen(TimeSelectionEndScreen):
    def __init__(self, parent, controller, **kw):
        TimeSelectionEndScreen.__init__(self, parent, controller, **kw)

    def init_widgets(self):
        super(TimeSelectionEndScreen, self).init_widgets()
        self.set_title(APPLY_SR_SCREEN_TITLE)
        self.set_instruction_1_text("What is the desired timestamp where the video should end?")

    def on_show_frame(self):
        self.set_error_message("")

    def on_hide_frame(self):
        pass

    def set_input_checks(self):
        self.add_input_check(lambda screen: frame_input_within_video_bounds_check(self))
        self.add_input_check(lambda screen: apply_sr_frame_range_valid_check(self))

    def on_input_check_success(self):
        self.controller.apply_sr_frame_range.last_frame_inclusive = calculate_frame_num_from_inputs(self)
