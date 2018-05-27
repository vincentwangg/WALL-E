from gui.abstract_screens.abstract_process_intro_screen import AbstractProcessIntroScreen
from gui.pipeline1.sr_scan_progress_screen import SrScanProgressScreen
from gui.pipeline1.utilities.constants import SR_FRAME_SELECTION_TITLE


class SrFrameSuggestionIntroScreen(AbstractProcessIntroScreen):
    def __init__(self, parent, controller, **kw):
        AbstractProcessIntroScreen.__init__(self, parent, controller,
                                            SR_FRAME_SELECTION_TITLE,
                                            [
                                                "For long videos, it may take hours to search\n"
                                                "for frames that contain a chessboard.",

                                                "As an option, you can help us save time by\n"
                                                "choosing a range of frames that is likely to have\n"
                                                "a chessboard in view.",

                                                "If you feel that this step isn't necessary,\n"
                                                "feel free to press skip."
                                            ],
                                            **kw)

    def on_next_button(self):
        self.controller.show_next_frame()

    def on_skip_button(self):
        self.controller.sr_scan_frame_range.reset_to_default()
        self.controller.show_frame(SrScanProgressScreen)
