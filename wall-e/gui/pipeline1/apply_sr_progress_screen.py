from gui.abstract_screens.progress_screen import ProgressScreen
from gui.pipeline1.constants import *
from stereo_rectification.apply_sr import apply_sr_gui_logic


class ApplySrProgressScreen(ProgressScreen):
    def __init__(self, parent, controller, **kw):
        ProgressScreen.__init__(self, parent, controller, apply_sr_gui_logic, **kw)
        self.set_title(APPLY_SR_PROGRESS_SCREEN_TITLE)
