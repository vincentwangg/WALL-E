from gui.abstract_screens.abstract_time_selection_start_screen import AbstractTimeSelectionStartScreen
from gui.abstract_screens.utilities.input_checks import frame_input_within_video_bounds_check
from gui.abstract_screens.utilities.time_input_util_methods import calculate_frame_num_from_inputs
from gui.pipeline1.utilities.constants import FRAME_MATCHING_SCREEN_TITLE


class FrameMatchingTimeStartScreen(AbstractTimeSelectionStartScreen):
    def __init__(self, parent, controller, **kw):
        AbstractTimeSelectionStartScreen.__init__(self, parent, controller, **kw)

    def init_widgets(self):
        AbstractTimeSelectionStartScreen.init_widgets(self)
        self.set_title(FRAME_MATCHING_SCREEN_TITLE)
        self.set_instruction_1_text("Please open the following video and find the timestamp\n"
                                    "a few seconds before a lot of light intensive\n"
                                    "activity starts to occur.")
        self.set_instruction_2_text("What was the timestamp?")

    def set_input_checks(self):
        self.add_input_check(lambda screen: frame_input_within_video_bounds_check(self))

    def on_input_check_success(self):
        self.controller.frame_matching_frame_range.first_frame = calculate_frame_num_from_inputs(self)
