from gui.abstract_screens.abstract_progress_screen import AbstractProgressScreen
from gui.pipeline1.utilities.constants import SR_PROGRESS_SCREEN_TITLE
from stereo_rectification.sr_map_gen import scan_video_for_checkerboard_frames


class SrScanProgressScreen(AbstractProgressScreen):
    def __init__(self, parent, controller, **kw):
        AbstractProgressScreen.__init__(self, parent, controller, scan_video_for_checkerboard_frames, **kw)
        self.set_title(SR_PROGRESS_SCREEN_TITLE)

    def on_next_button(self):
        if len(self.controller.builder.checkerboard_frames) < 1:
            from gui.pipeline1.sr_no_frames_found_screen import SrNoFramesFoundScreen
            self.controller.show_frame(SrNoFramesFoundScreen)
        else:
            self.controller.show_next_frame()
