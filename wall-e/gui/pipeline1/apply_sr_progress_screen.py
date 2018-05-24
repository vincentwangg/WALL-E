from gui.abstract_screens.abstract_progress_screen import AbstractProgressScreen
from gui.pipeline1.utilities.constants import *
from stereo_rectification.apply_sr import apply_sr_gui_logic


class ApplySrProgressScreen(AbstractProgressScreen):
    def __init__(self, parent, controller, **kw):
        AbstractProgressScreen.__init__(self, parent, controller, apply_sr_gui_logic, **kw)
        self.set_title(APPLY_SR_PROGRESS_SCREEN_TITLE)
