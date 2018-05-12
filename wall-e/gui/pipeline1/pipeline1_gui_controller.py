from tkinter import *
from gui.pipeline1.welcome_screen import WelcomeScreen
from gui.pipeline1.video_selection_screen import VideoSelectionScreen


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

        container = Frame(self, bg="red")
        container.grid(row=0, column=0)
        container['borderwidth'] = 2

        self.frames = {}
        for frame_class in (WelcomeScreen, VideoSelectionScreen):
            frame = frame_class(parent=container, controller=self)

            frame.grid(row=1, column=1)
            frame.grid_rowconfigure(0, weight=1)
            frame.grid_rowconfigure(1, weight=1)
            frame.grid_rowconfigure(2, weight=1)
            frame.grid_columnconfigure(0, weight=1)
            frame.grid_columnconfigure(1, weight=1)
            frame.grid_columnconfigure(2, weight=1)

            label = Label(container, bg="blue")
            label.grid(row=0, column=0)

            label = Label(container, bg="green")
            label.grid(row=2, column=2)

            self.frames[frame_class] = frame

        self.show_frame(VideoSelectionScreen)

    def show_frame(self, frame_class):
        self.frames[frame_class].tkraise()

    def set_video_filenames(self, left_video_fn, right_video_fn):
        self.left_video_filename = left_video_fn
        self.right_video_filename = right_video_fn
        print(self.left_video_filename)
        print(self.right_video_filename)
