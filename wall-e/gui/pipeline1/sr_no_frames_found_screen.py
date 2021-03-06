from gui.abstract_screens.abstract_title_description_next_screen import AbstractTitleDescriptionNextScreen
from gui.pipeline1.sr_frame_suggestion_intro_screen import SrFrameSuggestionIntroScreen
from gui.pipeline1.utilities.constants import SR_FRAME_SELECTION_TITLE


class SrNoFramesFoundScreen(AbstractTitleDescriptionNextScreen):
    def __init__(self, parent, controller, **kw):
        message_list = [
            "There were no frames found that were\n"
            "valid for stereo rectification. :(",
            "Please try again with a time range that has\n"
            "a better view of the full chessboard."
        ]

        AbstractTitleDescriptionNextScreen.__init__(self, parent, controller,
                                                    SR_FRAME_SELECTION_TITLE,
                                                    message_list,
                                                    **kw)

        self.next_button.configure(text="Try Again")

    def on_next_button(self):
        self.controller.show_frame(SrFrameSuggestionIntroScreen)
