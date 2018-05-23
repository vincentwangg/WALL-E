from gui.pipeline1.constants import SR_FRAME_SELECTION_TITLE
from gui.widgets.utilities import TimeSelectionStartScreen
from gui.widgets.utilities import calculate_frame_num_from_inputs, frame_input_within_video_bounds_check


class SrFrameSuggestionTimeStartScreen(TimeSelectionStartScreen):
    def __init__(self, parent, controller, **kw):
        TimeSelectionStartScreen.__init__(self, parent, controller, **kw)

    def init_widgets(self):
        super(SrFrameSuggestionTimeStartScreen, self).init_widgets()
        self.set_title(SR_FRAME_SELECTION_TITLE)
        self.set_instruction_1_text("Please open the following video and\n"
                                    "find the first timestamp where a chessboard appears.\n")
        self.set_instruction_2_text("What was the timestamp when this happened?")

    def on_show_frame(self):
        self.set_instruction_1_filename(self.controller.get_filename_of_video_with_0_offset() + "\n")
        self.set_error_message("")

    def on_hide_frame(self):
        pass

    def set_input_checks(self):
        self.add_input_check(lambda screen: frame_input_within_video_bounds_check(self))

    def on_input_check_success(self):
        self.controller.sr_scan_frame_range.first_frame = calculate_frame_num_from_inputs(self)
