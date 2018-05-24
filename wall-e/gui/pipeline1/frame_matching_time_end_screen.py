from gui.abstract_screens.abstract_time_selection_end_screen import AbstractTimeSelectionEndScreen
from gui.abstract_screens.utilities.input_checks import frame_input_within_video_bounds_check, \
    frame_matching_frame_range_valid_check
from gui.abstract_screens.utilities.time_input_util_methods import calculate_frame_num_from_inputs
from gui.pipeline1.utilities.constants import FRAME_MATCHING_SCREEN_TITLE


class FrameMatchingTimeEndScreen(AbstractTimeSelectionEndScreen):
    def __init__(self, parent, controller, **kw):
        AbstractTimeSelectionEndScreen.__init__(self, parent, controller, **kw)

    def init_widgets(self):
        AbstractTimeSelectionEndScreen.init_widgets(self)
        self.set_title(FRAME_MATCHING_SCREEN_TITLE)
        self.set_instruction_1_text("What was the time stamp a few seconds after the\n"
                                    "light intensive activity stops?")

    def set_input_checks(self):
        self.add_input_check(lambda screen: frame_input_within_video_bounds_check(self))
        self.add_input_check(lambda screen: frame_matching_frame_range_valid_check(self))

    def on_input_check_success(self):
        self.controller.frame_matching_frame_range.last_frame_inclusive = calculate_frame_num_from_inputs(self)
