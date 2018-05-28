from Tkinter import Button

from gui.abstract_screens.abstract_process_intro_screen import AbstractProcessIntroScreen
from gui.pipeline1.frame_matching_progress_screen import FrameMatchingProgressScreen
from gui.pipeline1.utilities.constants import FRAME_MATCHING_SCREEN_TITLE
from gui.pipeline1.frame_matching_validation_screen import FrameMatchingValidationScreen


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
                                                
                                                "Choose one of the options below\n"
                                                "for frame matching."
                                            ],
                                            **kwargs)

    def init_widgets(self):
        AbstractProcessIntroScreen.init_widgets(self)
        self.next_button.configure(text="Use custom time range")
        self.skip_button.configure(text="Loop through full video")
        self.custom_sr_map_button = Button(self.content_wrapper, text="Manually choose video offsets",
                                           command=lambda: self.controller.show_frame(FrameMatchingValidationScreen))

    def add_widgets_to_frame(self):
        AbstractProcessIntroScreen.add_widgets_to_frame(self)
        self.custom_sr_map_button.pack()

    def on_next_button(self):
        self.controller.show_next_frame()

    def on_skip_button(self):
        self.controller.frame_matching_frame_range.reset_to_default()
        self.controller.show_frame(FrameMatchingProgressScreen)
