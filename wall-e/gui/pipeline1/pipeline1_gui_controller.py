from Tkinter import Tk, Frame

from gui.pipeline1.apply_sr_intro_screen import ApplySrIntroScreen
from gui.pipeline1.apply_sr_progress_screen import ApplySrProgressScreen
from gui.pipeline1.apply_sr_time_end_screen import ApplySrTimeEndScreen
from gui.pipeline1.apply_sr_time_start_screen import ApplySrTimeStartScreen
from gui.pipeline1.final_screen import FinalScreen
from gui.pipeline1.frame_matching_intro_screen import FrameMatchingIntroScreen
from gui.pipeline1.frame_matching_progress_screen import FrameMatchingProgressScreen
from gui.pipeline1.frame_matching_time_end_screen import FrameMatchingTimeEndScreen
from gui.pipeline1.frame_matching_time_start_screen import FrameMatchingTimeStartScreen
from gui.pipeline1.frame_matching_validation_screen import FrameMatchingValidationScreen
from gui.pipeline1.sr_frame_selection_screen import SrFrameSelection
from gui.pipeline1.sr_frame_selected_screen import SrFrameSelectedScreen
from gui.pipeline1.sr_frame_suggestion_intro_screen import SrFrameSuggestionIntroScreen
from gui.pipeline1.sr_frame_suggestion_time_end_screen import SrFrameSuggestionTimeEndScreen
from gui.pipeline1.sr_frame_suggestion_time_start_screen import SrFrameSuggestionTimeStartScreen
from gui.pipeline1.sr_no_frames_found_screen import SrNoFramesFoundScreen
from gui.pipeline1.sr_scan_progress_screen import SrScanProgressScreen
from gui.pipeline1.utilities.constants import WINDOW_WIDTH, WINDOW_HEIGHT
from gui.pipeline1.video_scan_progress_screen import VideoScanProgressScreen
from gui.pipeline1.video_selection_screen import VideoSelectionScreen
from gui.pipeline1.welcome_screen import WelcomeScreen
from gui.widgets.walle_header import WalleHeader
from utils_general.video_frame_loader import VideoFrameLoader

screen_classes_in_order = [
    WelcomeScreen,
    VideoSelectionScreen,
    VideoScanProgressScreen,
    FrameMatchingIntroScreen,
    FrameMatchingTimeStartScreen,
    FrameMatchingTimeEndScreen,
    FrameMatchingProgressScreen,
    FrameMatchingValidationScreen,
    SrFrameSuggestionIntroScreen,
    SrFrameSuggestionTimeStartScreen,
    SrFrameSuggestionTimeEndScreen,
    SrScanProgressScreen,
    # SrFrameSelection,
    SrFrameSelectedScreen,
    ApplySrIntroScreen,
    ApplySrTimeStartScreen,
    ApplySrTimeEndScreen,
    ApplySrProgressScreen,
    FinalScreen
]
other_screens_to_render = [
    SrNoFramesFoundScreen
]
first_screen = WelcomeScreen


class Pipeline1GuiController(Tk):
    def __init__(self):
        Tk.__init__(self)

        self.video_frame_loader = None
        self.top_frame = None
        self.video_offsets = VideoOffsets()
        self.sr_results = None
        self.sr_map = None

        self.frame_matching_frame_range = FrameRange()
        self.sr_scan_frame_range = FrameRange()
        self.apply_sr_frame_range = FrameRange()

        self.left_video_filename_sr = None
        self.right_video_filename_sr = None

        self.title("Video Processing Part 1 (of 2)")
        self.resizable(0, 0)
        self.geometry(str(WINDOW_WIDTH) + "x" + str(WINDOW_HEIGHT))

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.screen_container = Frame(self)
        self.screen_container.pack(fill="both", expand=True)

        self.walle_header = WalleHeader(parent=self.screen_container, controller=self)
        self.walle_header.grid(row=0, column=0, sticky="w")

        self.frames = {}
        self.prepare_screens(screen_classes_in_order)
        self.prepare_screens(other_screens_to_render)

        self.adjust_frame_content_dimensions()
        self.center_in_computer_screen(self.winfo_width(), self.winfo_height())

        self.set_and_start_top_frame(first_screen)

    def prepare_screens(self, screen_frames):
        for frame_class in screen_frames:
            frame = frame_class(parent=self.screen_container, controller=self, borderwidth=2, relief="groove")
            frame.grid(row=1, column=0, sticky="nsew")

            self.frames[frame_class] = frame

    def show_next_frame(self):
        idx = screen_classes_in_order.index(self.top_frame)
        if idx < len(screen_classes_in_order) - 1:
            next_frame_class = screen_classes_in_order[idx + 1]
            self.show_frame(next_frame_class)

    def show_prev_frame(self):
        idx = screen_classes_in_order.index(self.top_frame)
        if idx > 0:
            prev_frame_class = screen_classes_in_order[idx - 1]
            self.show_frame(prev_frame_class)

    def show_frame(self, frame_class):
        self.frames[self.top_frame].on_hide_frame()
        self.set_and_start_top_frame(frame_class)

    def set_and_start_top_frame(self, frame_class):
        self.top_frame = frame_class
        self.frames[frame_class].tkraise()
        self.frames[frame_class].on_show_frame()

    def update_frame(self, data):
        self.frames[self.top_frame].update_frame(data)

    def set_video_filenames(self, left_video_fn, right_video_fn):
        self.video_frame_loader = VideoFrameLoader(left_video_fn, right_video_fn)

    # Informs all the frames of the actual width and height they should be using
    def adjust_frame_content_dimensions(self):
        self.update()
        window_height = self.winfo_height()
        window_width = self.winfo_width()
        walle_header_height = self.walle_header.winfo_height()

        frame_height = window_height - walle_header_height

        for key in self.frames:
            self.frames[key].set_dimensions(width=window_width, height=frame_height)

    def center_in_computer_screen(self, width, height):
        self.update_idletasks()
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        size = (width, height)
        x = w / 2 - size[0] / 2
        y = h / 2 - size[1] / 2
        self.geometry("%dx%d+%d+%d" % (size + (x, y)))

    def get_filename_of_video_with_0_offset(self):
        if self.video_offsets.left_offset == 0:
            return self.video_frame_loader.left_feed_filename
        else:
            return self.video_frame_loader.right_feed_filename

    def get_file_basename_of_video_with_0_offset(self):
        if self.video_offsets.left_offset == 0:
            return self.video_frame_loader.left_feed_basename
        else:
            return self.video_frame_loader.right_feed_basename

    def is_frame_num_within_video_bounds(self, frame_num):
        if frame_num < 0:
            return False

        if frame_num + self.video_offsets.left_offset > self.video_frame_loader.last_frame_num_left:
            return False
        if frame_num + self.video_offsets.right_offset > self.video_frame_loader.last_frame_num_right:
            return False

        return True


class VideoOffsets:
    def __init__(self, left_offset=0, right_offset=0):
        self.left_offset = left_offset
        self.right_offset = right_offset


class FrameRange:
    def __init__(self, first_frame=0, last_frame_inclusive=-1):
        self.first_frame = first_frame

        # if last_frame_inclusive is -1, then the last frame should be the last frame in the video
        self.last_frame_inclusive = last_frame_inclusive

    def reset_to_default(self):
        self.first_frame = 0
        self.last_frame_inclusive = -1
