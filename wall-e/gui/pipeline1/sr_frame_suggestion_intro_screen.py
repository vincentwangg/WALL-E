import os
from tkFileDialog import askopenfilename

from definitions import ROOT_DIR
from gui.abstract_screens.abstract_title_description_multiple_buttons_screen import \
    AbstractTitleDescriptionMultipleButtonsScreen
from gui.pipeline1.apply_sr_intro_screen import ApplySrIntroScreen
from gui.pipeline1.sr_scan_progress_screen import SrScanProgressScreen
from gui.pipeline1.utilities.constants import SR_MAP_GEN_TITLE
from stereo_rectification.apply_sr import generate_sr_map_dict_from_file


class SrFrameSuggestionIntroScreen(AbstractTitleDescriptionMultipleButtonsScreen):
    def __init__(self, parent, controller, **kw):
        message_list = [
            "For long videos, it may take hours to search\n"
            "for frames that contain a chessboard.",

            "As an option, you can save time by choosing\n"
            "a time range that is likely to have\n"
            "a chessboard in view.",

            "Choose one of the options below as your\n"
            "choice of finding a SR map."
        ]
        button_text_list = [
            "Choose custom time range",
            "Scan through full video",
            "Choose custom YML SR map"
        ]
        button_command_list = [
            self.choose_custom_time_range,
            self.scan_through_full_video,
            self.set_custom_sr_map
        ]

        AbstractTitleDescriptionMultipleButtonsScreen.__init__(self, parent, controller,
                                                               SR_MAP_GEN_TITLE,
                                                               message_list,
                                                               button_text_list,
                                                               button_command_list,
                                                               **kw)

    def init_widgets(self):
        AbstractTitleDescriptionMultipleButtonsScreen.init_widgets(self)

    def add_widgets_to_frame(self):
        AbstractTitleDescriptionMultipleButtonsScreen.add_widgets_to_frame(self)

    def choose_custom_time_range(self):
        self.controller.show_next_frame()

    def scan_through_full_video(self):
        self.controller.sr_scan_frame_range.reset_to_default()
        self.controller.show_frame(SrScanProgressScreen)

    def set_custom_sr_map(self):
        filename = askopenfilename(initialdir=os.path.dirname(ROOT_DIR), title="Select YML file",
                                   filetypes=[("YML files", "*.yml")])

        if os.path.isfile(filename):
            self.controller.sr_map = generate_sr_map_dict_from_file(filename)
            self.controller.show_frame(ApplySrIntroScreen)
