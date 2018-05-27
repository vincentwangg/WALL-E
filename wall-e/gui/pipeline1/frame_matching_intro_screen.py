from gui.abstract_screens.abstract_process_intro_screen import AbstractProcessIntroScreen
from gui.pipeline1.frame_matching_progress_screen import FrameMatchingProgressScreen
from gui.pipeline1.utilities.constants import FRAME_MATCHING_SCREEN_TITLE


class FrameMatchingIntroScreen(AbstractProcessIntroScreen):
    def __init__(self, parent, controller, **kwargs):
        AbstractProcessIntroScreen.__init__(self, parent, controller,
                                            FRAME_MATCHING_SCREEN_TITLE,
                                            [
                                                "Simultaneously starting two cameras to record is a simple\n"
                                                "process, but one recording might start several\n"
                                                "frames earlier than the other recording.",

                                                "To resolve this, the frame matching process will find and\n"
                                                "detect light intensity differences in each frame to\n"
                                                "find an offset that will most effectively\n"
                                                "line up the videos.",
                                                
                                                "If you would like to manually find the offset,\n"
                                                "feel free to press skip."
                                            ],
                                            **kwargs)

    def on_next_button(self):
        self.controller.show_next_frame()

    def on_skip_button(self):
        self.controller.frame_matching_frame_range.reset_to_default()
        self.controller.show_frame(FrameMatchingProgressScreen)
