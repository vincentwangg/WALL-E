from gui.abstract_screens.abstract_progress_screen import AbstractProgressScreen
from gui.pipeline1.utilities.constants import SR_BUILD_MAP_PROGRESS_SCREEN_TITLE
from stereo_rectification.sr_map_gen import build_sr_map


class SrBuildMapProgressScreen(AbstractProgressScreen):
    def __init__(self, parent, controller, **kw):
        AbstractProgressScreen.__init__(self, parent, controller, build_sr_map, **kw)
        self.set_title(SR_BUILD_MAP_PROGRESS_SCREEN_TITLE)

    def on_next_button(self):
        if self.controller.sr_map is None:
            from gui.pipeline1.sr_no_frames_found_screen import SrNoFramesFoundScreen
            self.controller.show_frame(SrNoFramesFoundScreen)
        else:
            self.controller.show_next_frame()