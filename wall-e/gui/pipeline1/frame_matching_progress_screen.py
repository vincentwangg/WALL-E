from frame_matching.frame_match_intensity import frame_match_gui_backend_logic
from gui.abstract_screens.abstract_progress_screen import AbstractProgressScreen
from gui.pipeline1.utilities.constants import FRAME_MATCHING_SCREEN_TITLE


class FrameMatchingProgressScreen(AbstractProgressScreen):
    def __init__(self, parent, controller, **kw):
        AbstractProgressScreen.__init__(self, parent, controller, frame_match_gui_backend_logic, **kw)
        self.set_title(FRAME_MATCHING_SCREEN_TITLE)
