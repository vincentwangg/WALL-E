from gui.abstract_screens.abstract_title_description_multiple_buttons_screen import \
    AbstractTitleDescriptionMultipleButtonsScreen
from gui.abstract_screens.abstract_title_description_two_buttons_screen import AbstractTitleDescriptionTwoButtonsScreen
from gui.pipeline1.apply_sr_progress_screen import ApplySrProgressScreen
from gui.pipeline1.apply_sr_time_start_screen import ApplySrTimeStartScreen
from gui.pipeline1.utilities.constants import APPLY_SR_SCREEN_TITLE


class ApplySrIntroScreen(AbstractTitleDescriptionMultipleButtonsScreen):
    def __init__(self, parent, controller, **kw):
        message_list = [
            "For long videos, it may take hours to create\n"
            "a new stereo rectified video.",

            "In the next few screens, you may enter timestamps to\n"
            "crop the video to save time on\n"
            "creating the stereo rectified footage.",

            "If you feel that this step isn't necessary,\n"
            "feel free to press skip."
        ]
        button_text_list = [
            "Choose custom time range to crop video",
            "Create full SR'd video"
        ]
        button_command_list = [
            self.choose_custom_time_range,
            self.scan_through_full_video,
        ]

        AbstractTitleDescriptionMultipleButtonsScreen.__init__(self, parent, controller,
                                                               APPLY_SR_SCREEN_TITLE,
                                                               message_list,
                                                               button_text_list,
                                                               button_command_list,
                                                               **kw)

    def choose_custom_time_range(self):
        self.controller.show_frame(ApplySrTimeStartScreen)

    def scan_through_full_video(self):
        self.controller.apply_sr_frame_range.reset_to_default()
        self.controller.show_frame(ApplySrProgressScreen)
