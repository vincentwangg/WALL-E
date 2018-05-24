from gui.abstract_screens.abstract_time_selection_end_screen import AbstractTimeSelectionEndScreen
from gui.abstract_screens.utilities.input_checks import frame_input_within_video_bounds_check, \
    apply_sr_frame_range_valid_check
from gui.abstract_screens.utilities.time_input_util_methods import calculate_frame_num_from_inputs
from gui.pipeline1.utilities.constants import APPLY_SR_SCREEN_TITLE


class ApplySrTimeEndScreen(AbstractTimeSelectionEndScreen):
    def __init__(self, parent, controller, **kw):
        AbstractTimeSelectionEndScreen.__init__(self, parent, controller, **kw)

    def init_widgets(self):
        AbstractTimeSelectionEndScreen.init_widgets(self)
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
