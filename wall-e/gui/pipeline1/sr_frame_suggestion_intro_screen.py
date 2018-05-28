import os
from Tkinter import Button
from tkFileDialog import askopenfilename

from definitions import ROOT_DIR
from gui.abstract_screens.abstract_process_intro_screen import AbstractProcessIntroScreen
from gui.pipeline1.apply_sr_intro_screen import ApplySrIntroScreen
from gui.pipeline1.sr_scan_progress_screen import SrScanProgressScreen
from gui.pipeline1.utilities.constants import SR_FRAME_SELECTION_TITLE
from stereo_rectification.apply_sr import generate_sr_map_dict_from_file


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
                                                "feel free to press skip\n"
                                                "(or select your own .yml SR map)."
                                            ],
                                            **kw)

    def init_widgets(self):
        AbstractProcessIntroScreen.init_widgets(self)
        self.custom_sr_map_button = Button(self.content_wrapper, text="Choose custom YML SR map",
                                           command=self.set_custom_sr_map)

    def add_widgets_to_frame(self):
        AbstractProcessIntroScreen.add_widgets_to_frame(self)
        self.custom_sr_map_button.pack()

    def on_next_button(self):
        self.controller.show_next_frame()

    def on_skip_button(self):
        self.controller.sr_scan_frame_range.reset_to_default()
        self.controller.show_frame(SrScanProgressScreen)

    def set_custom_sr_map(self):
        filename = askopenfilename(initialdir=os.path.dirname(ROOT_DIR), title="Select YML file",
                                   filetypes=[("YML files", "*.yml")])

        if os.path.isfile(filename):
            self.controller.sr_map = generate_sr_map_dict_from_file(filename)
            self.controller.show_frame(ApplySrIntroScreen)
