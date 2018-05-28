from gui.abstract_screens.abstract_title_description_multiple_buttons_screen import \
    AbstractTitleDescriptionMultipleButtonsScreen
from gui.pipeline1.frame_matching_progress_screen import FrameMatchingProgressScreen
from gui.pipeline1.frame_matching_time_start_screen import FrameMatchingTimeStartScreen
from gui.pipeline1.frame_matching_validation_screen import FrameMatchingValidationScreen
from gui.pipeline1.utilities.constants import FRAME_MATCHING_SCREEN_TITLE


class FrameMatchingIntroScreen(AbstractTitleDescriptionMultipleButtonsScreen):
    def __init__(self, parent, controller, **kwargs):
        message_list = [
            "Simultaneously starting two cameras to record is a simple\n"
            "process, but one recording might start several\n"
            "frames earlier than the other recording.",

            "To resolve this, the frame matching process will find and\n"
            "detect light intensity differences in each frame to\n"
            "find an offset that will most effectively\n"
            "line up the videos.",

            "Choose one of the options below\n"
            "to find a video offset."
        ]
        button_text_list = [
            "Choose custom time range",
            "Scan through full video",
            "Manually choose video offsets"
        ]
        button_command_list = [
            self.choose_custom_time_range,
            self.scan_through_full_video,
            self.manually_choose_video_offsets
        ]

        AbstractTitleDescriptionMultipleButtonsScreen.__init__(self, parent, controller,
                                                               FRAME_MATCHING_SCREEN_TITLE,
                                                               message_list,
                                                               button_text_list,
                                                               button_command_list,
                                                               **kwargs)

    def choose_custom_time_range(self):
        self.controller.show_frame(FrameMatchingTimeStartScreen)

    def scan_through_full_video(self):
        self.controller.frame_matching_frame_range.reset_to_default()
        self.controller.show_frame(FrameMatchingProgressScreen)

    def manually_choose_video_offsets(self):
        self.controller.show_frame(FrameMatchingValidationScreen)
