from gui.pipeline1.constants import SR_FRAME_SELECTION_TITLE
from gui.pipeline1.utilities.inputs import calculate_frame_num_from_inputs, frame_input_within_video_bounds_check, sr_scan_frame_range_valid_check
from gui.pipeline1.utilities.time_selection_end_screen import TimeSelectionEndScreen

ENTRY_WIDTH = 5


class SrFrameSuggestionTimeEndScreen(TimeSelectionEndScreen):
    def __init__(self, parent, controller, **kw):
        TimeSelectionEndScreen.__init__(self, parent, controller, **kw)

    def init_widgets(self):
        super(SrFrameSuggestionTimeEndScreen, self).init_widgets()

    def add_widgets_to_frame(self):
        super(SrFrameSuggestionTimeEndScreen, self).add_widgets_to_frame()

    def on_show_frame(self):
        self.set_title(SR_FRAME_SELECTION_TITLE)
        self.set_instruction_1_text("What was the time stamp when the chessboard went out of view?")
        self.set_error_message("")

    def set_input_checks(self):
        self.add_input_check(lambda screen: frame_input_within_video_bounds_check(self))
        self.add_input_check(lambda screen: sr_scan_frame_range_valid_check(self))

    def on_input_check_success(self):
        super()
        self.controller.sr_scan_frame_range.last_frame_inclusive = calculate_frame_num_from_inputs(self)
