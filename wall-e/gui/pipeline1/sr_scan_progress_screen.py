from gui.abstract_screens.progress_screen import ProgressScreen
from gui.pipeline1.constants import *
from stereo_rectification.sr_map_gen import get_list_of_valid_frames_for_sr_tkinter


class SrScanProgressScreen(ProgressScreen):
    def __init__(self, parent, controller, **kw):
        ProgressScreen.__init__(self, parent, controller, get_list_of_valid_frames_for_sr_tkinter, **kw)
        self.set_title(SR_PROGRESS_SCREEN_TITLE)
