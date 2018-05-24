from gui.abstract_screens.abstract_process_intro_screen import AbstractProcessIntroScreen
from gui.pipeline1.apply_sr_progress_screen import ApplySrProgressScreen
from gui.pipeline1.utilities.constants import APPLY_SR_SCREEN_TITLE


class ApplySrIntroScreen(AbstractProcessIntroScreen):
    def __init__(self, parent, controller, **kw):
        AbstractProcessIntroScreen.__init__(self, parent, controller,
                                            APPLY_SR_SCREEN_TITLE,
                                            [
                                        "For long videos, it may take hours to create\n"
                                        "a new stereo rectified video.",

                                        "In the next few screens, you may enter timestamps to\n"
                                        "crop the video to save time on\n"
                                        "creating the stereo rectified footage.",

                                        "If you feel that this step isn't necessary,\n"
                                        "feel free to press skip."
                                    ],
                                            **kw)

    def on_next_button(self):
        self.controller.show_next_frame()

    def on_skip_button(self):
        self.controller.apply_sr_frame_range.reset_to_default()
        self.controller.show_frame(ApplySrProgressScreen)
