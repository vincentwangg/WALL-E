from tkinter import *

from gui.pipeline1.video_frame_player_screen import VideoFramePlayer
from gui.pipeline1.video_scan_screen import VideoScanScreen
from gui.pipeline1.video_selection_screen import VideoSelectionScreen
from gui.pipeline1.welcome_screen import WelcomeScreen
from gui.walle_header import WalleHeader
from utilities.video_frame_loader import VideoFrameLoader


class Pipeline1GuiController(Tk):
    def __init__(self):
        Tk.__init__(self)

        self.video_frame_loader = None
        self.top_frame = None

        self.title("Video Processing Part 1 (of 2)")
        self.resizable(0, 0)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        container = Frame(self)
        container.pack(fill="both", expand=True)

        walle_header = WalleHeader(parent=container, controller=self)
        walle_header.grid(row=0, column=0, sticky="w")

        self.frames = {}
        for frame_class in (WelcomeScreen, VideoSelectionScreen, VideoScanScreen, VideoFramePlayer):
            frame = frame_class(parent=container, controller=self, borderwidth=2, relief="groove")
            frame.grid(row=1, column=0, sticky="nsew")

            self.frames[frame_class] = frame

        self.adjust_frame_content_dimensions()
        self.center_in_computer_screen(self.winfo_width(), self.winfo_height())

        self.set_and_start_top_frame(VideoSelectionScreen)

    def show_frame(self, frame_class):
        self.stop_top_frame()
        self.set_and_start_top_frame(frame_class)

    def set_and_start_top_frame(self, frame_class):
        self.top_frame = frame_class
        self.frames[frame_class].tkraise()
        self.frames[frame_class].start()

    def stop_top_frame(self):
        self.frames[self.top_frame].stop()

    def update_frame(self, data):
        self.frames[self.top_frame].update_frame(data)

    def set_video_filenames(self, left_video_fn, right_video_fn):
        self.video_frame_loader = VideoFrameLoader(left_video_fn, right_video_fn)

    # Informs all the frames of the actual width and height they should be using
    def adjust_frame_content_dimensions(self):
        self.update()
        window_height = self.winfo_height()
        window_width = self.winfo_width()
        walle_header_height = self.winfo_height()

        frame_height = window_height-walle_header_height

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

class VideoOffsets:
    def __init__(self, left_offset=0, right_offset=0):
        self.left_offset = left_offset
        self.right_offset = right_offset