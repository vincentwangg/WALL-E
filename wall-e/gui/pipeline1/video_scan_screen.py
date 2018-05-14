import threading
import time
import datetime
from tkinter.ttk import *
from tkinter import *
from gui.gui_base_frame import GuiBaseFrame
from gui.pipeline1.constants import *
from gui.pipeline1.video_frame_player_screen import VideoFramePlayer
from gui.widgets.header1_label import Header1Label
from gui.widgets.p_label import PLabel


class VideoScanScreen(GuiBaseFrame):
    def __init__(self, parent, controller, **kw):
        GuiBaseFrame.__init__(self, parent, controller, **kw)
        self.counting_left_frames = None

    def setup_widgets(self):
        self.content_wrapper = Frame(self)
        self.content_wrapper.configure(bg="white")
        self.screen_title = Header1Label(self.content_wrapper,
                                         text="Scanning video for information...\n")
        self.progress_bar = Progressbar(self.content_wrapper, orient=HORIZONTAL, mode="indeterminate",
                                        length=WINDOW_WIDTH / 2)
        self.wait_text = PLabel(self.content_wrapper, text="\nThis might take a few minutes."
                                                           "\nPlease do not change the video files while this is running.\n")
        self.left_frames_count = PLabel(self.content_wrapper, text=LEFT_FRAMES_COUNT_PREFIX + "0")
        self.right_frames_count = PLabel(self.content_wrapper, text=RIGHT_FRAMES_COUNT_PREFIX + "0")
        self.elapsed_time_label = PLabel(self.content_wrapper)
        self.empty_space = PLabel(self.content_wrapper, text=" ")
        self.next_button = Button(self.content_wrapper, text="Next", state=DISABLED,
                                  # TODO change to frame matching screen
                                  command=lambda: self.controller.show_frame(VideoFramePlayer))

        self.screen_title.pack()
        self.progress_bar.pack()
        self.wait_text.pack()
        self.left_frames_count.pack()
        self.right_frames_count.pack()
        self.elapsed_time_label.pack()
        self.empty_space.pack()
        self.next_button.pack()
        self.content_wrapper.place(relx=0.5, rely=0.4, anchor=CENTER)

    def start(self):
        self.start_time = time.time()
        self.progress_bar.start()
        self.frame_count_thread = threading.Thread(target=self.controller.video_frame_loader.count_frames_in_videos,
                                                   kwargs={"controller": self.controller})
        self.frame_count_thread.start()
        self.master.after(50, self.check_thread)

    def update_frame(self, data):
        if LEFT_FRAMES_COUNT_PREFIX in data:
            self.left_frames_count.configure(text=data)
        if RIGHT_FRAMES_COUNT_PREFIX in data:
            self.right_frames_count.configure(text=data)

        self.elapsed_time_label.configure(text=ELAPSED_TIME_PREFIX +
                                               str(datetime.timedelta(seconds=int(time.time() - self.start_time))))

    def stop(self):
        self.progress_bar.stop()

    def check_thread(self):
        if self.frame_count_thread.is_alive():
            self.master.after(50, self.check_thread)
        else:
            self.progress_bar.stop()
            self.wait_text.configure(text="\nDone!\n\n")
            self.next_button.configure(state=NORMAL)