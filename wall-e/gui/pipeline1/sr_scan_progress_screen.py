from gui.abstract_screens.abstract_progress_screen import AbstractProgressScreen
from gui.pipeline1.utilities.constants import *
from stereo_rectification.sr_map_gen import get_list_of_valid_frames_for_sr_tkinter


class SrScanProgressScreen(AbstractProgressScreen):
    def __init__(self, parent, controller, **kw):
        AbstractProgressScreen.__init__(self, parent, controller, get_list_of_valid_frames_for_sr_tkinter, **kw)
        self.set_title(SR_PROGRESS_SCREEN_TITLE)
