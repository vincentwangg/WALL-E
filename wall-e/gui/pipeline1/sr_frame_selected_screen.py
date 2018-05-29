from gui.abstract_screens.abstract_title_description_next_screen import AbstractTitleDescriptionNextScreen
from gui.pipeline1.apply_sr_intro_screen import ApplySrIntroScreen
from gui.pipeline1.utilities.constants import SR_FRAME_SELECTION_TITLE
from stereo_rectification.sr_map import SR_MAP_FILENAME


class SrFrameSelectedScreen(AbstractTitleDescriptionNextScreen):
    def __init__(self, parent, controller, **kw):
        message_list = [
            "The selected stereo rectification map has\nbeen saved to the path:\n" + SR_MAP_FILENAME
        ]

        AbstractTitleDescriptionNextScreen.__init__(self, parent, controller,
                                                    SR_FRAME_SELECTION_TITLE,
                                                    message_list,
                                                    **kw)

    def on_next_button(self):
        self.controller.show_frame(ApplySrIntroScreen)
