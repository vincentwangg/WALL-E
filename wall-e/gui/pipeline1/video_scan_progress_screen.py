import datetime
import threading
import time
from Tkinter import Frame, HORIZONTAL, DISABLED, CENTER, NORMAL, Button
from ttk import Progressbar

from gui.abstract_screens.utilities.constants import ELAPSED_TIME_PREFIX
from gui.pipeline1.utilities.constants import WINDOW_WIDTH, LEFT_FRAMES_COUNT_PREFIX, RIGHT_FRAMES_COUNT_PREFIX, \
    SCREENS_REL_X, \
    SCREENS_REL_Y
from gui.widgets.gui_base_frame import GuiBaseFrame
from gui.widgets.header1_label import Header1Label
from gui.widgets.p_label import PLabel


class VideoScanProgressScreen(GuiBaseFrame):
    def __init__(self, parent, controller, **kw):
        GuiBaseFrame.__init__(self, parent, controller, **kw)
        self.counting_left_frames = None

    def init_widgets(self):
        self.content_wrapper = Frame(self)
        self.content_wrapper.configure(background="white")
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
                                  command=lambda: self.controller.show_next_frame())

    def add_widgets_to_frame(self):
        self.screen_title.pack()
        self.progress_bar.pack()
        self.wait_text.pack()
        self.left_frames_count.pack()
        self.right_frames_count.pack()
        self.elapsed_time_label.pack()
        self.empty_space.pack()
        self.next_button.pack()
        self.content_wrapper.place(relx=SCREENS_REL_X, rely=SCREENS_REL_Y, anchor=CENTER)

    def on_show_frame(self):
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

    def on_hide_frame(self):
        self.progress_bar.stop()

    def check_thread(self):
        if self.frame_count_thread.is_alive():
            self.master.after(50, self.check_thread)
        else:
            self.progress_bar.stop()
            self.wait_text.configure(text="\nDone!\n\n")
            self.next_button.configure(state=NORMAL)
