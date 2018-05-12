from tkinter import *
from gui.pipeline1.welcome_screen import WelcomeScreen
from gui.pipeline1.video_selection_screen import VideoSelectionScreen
from gui.walle_header import WalleHeader
from utilities.video_frame_player_gui import VideoFramePlayer


class Pipeline1GuiController(Tk):
    def __init__(self):
        Tk.__init__(self)

        self.left_video_filename = None
        self.right_video_filename = None

        self.resizable(0, 0)

        self.title("Video Processing Part 1 (of 2)")

        # self.geometry("500x500")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        container = Frame(self)
        container.pack(fill="both", expand=True)

        walle_header = WalleHeader(parent=container, controller=self)
        walle_header.grid(row=0, column=0, sticky="w")

        self.frames = {}
        for frame_class in (WelcomeScreen, VideoSelectionScreen, VideoFramePlayer):
            frame = frame_class(parent=container, controller=self)
            frame.grid(row=1, column=0, sticky="nsew")

            self.frames[frame_class] = frame

        self.adjust_frame_dimensions()

        self.center(self.winfo_width(), self.winfo_height())

        self.show_frame(WelcomeScreen)

    def show_frame(self, frame_class):
        self.frames[frame_class].tkraise()

    def set_video_filenames(self, left_video_fn, right_video_fn):
        self.left_video_filename = left_video_fn
        self.right_video_filename = right_video_fn
        self.frames[VideoFramePlayer].set_video_filenames(left_video_fn, right_video_fn)

        # TODO Link frame matching offset results
        self.frames[VideoFramePlayer].start_video()

    def adjust_frame_dimensions(self):
        self.update()
        window_height = self.winfo_height()
        window_width = self.winfo_width()
        walle_header_height = self.winfo_height()

        frame_height = window_height-walle_header_height

        for key in self.frames:
            self.frames[key].set_dimensions(width=window_width, height=frame_height)

    def center(self, width, height):
        self.update_idletasks()
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        size = (width, height)
        x = w / 2 - size[0] / 2
        y = h / 2 - size[1] / 2
        self.geometry("%dx%d+%d+%d" % (size + (x, y)))
