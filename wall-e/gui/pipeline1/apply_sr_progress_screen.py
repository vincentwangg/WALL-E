import datetime
import threading
import time
from tkinter import *
from tkinter.ttk import Progressbar

from gui.pipeline1.constants import *
from gui.widgets.gui_base_frame import GuiBaseFrame
from gui.widgets.header1_label import Header1Label
from gui.widgets.p_label import PLabel
from stereo_rectification.apply_sr import apply_sr_gui_logic


class ApplySrProgressScreen(GuiBaseFrame):
    def __init__(self, parent, controller, **kw):
        GuiBaseFrame.__init__(self, parent, controller, **kw)

    def init_widgets(self):
        self.content_wrapper = Frame(self)
        self.content_wrapper.configure(bg="white")

        self.screen_title = Header1Label(self.content_wrapper,
                                         text="Applying stereo rectification to your videos...\n")
        self.progress_bar_control_var = DoubleVar()
        self.progress_bar = Progressbar(self.content_wrapper, orient=HORIZONTAL, mode="determinate",
                                        length=WINDOW_WIDTH / 2, variable=self.progress_bar_control_var)
        self.wait_text = PLabel(self.content_wrapper, text="\nThis might take a few minutes."
                                                           "\nPlease do not change the video files while this is "
                                                           "running.\n")
        self.frames_applied = PLabel(self.content_wrapper)
        self.elapsed_time_label = PLabel(self.content_wrapper)
        self.estimated_time_left_label = PLabel(self.content_wrapper)
        self.empty_space = PLabel(self.content_wrapper)
        self.next_button = Button(self.content_wrapper, text="Next", state=DISABLED,
                                  command=lambda: self.controller.show_next_frame())

    def add_widgets_to_frame(self):
        self.screen_title.pack()
        self.progress_bar.pack()
        self.wait_text.pack()
        self.frames_applied.pack()
        self.elapsed_time_label.pack()
        self.estimated_time_left_label.pack()
        self.empty_space.pack()
        self.next_button.pack()
        self.content_wrapper.place(relx=SCREENS_REL_X, rely=SCREENS_REL_Y, anchor=CENTER)

    def on_show_frame(self):
        self.start_time = time.time()
        self.sr_frame_count_thread = threading.Thread(target=apply_sr_gui_logic,
                                                      kwargs={"controller": self.controller})
        self.sr_frame_count_thread.start()
        self.master.after(50, self.check_thread)

    def update_frame(self, data):
        frames_processed = data[APPLY_SR_PROGRESS_FRAMES_PROCESSED]
        total_frames = data[APPLY_SR_PROGRESS_TOTAL_FRAMES]

        # Prevent divide by 0 error
        total_frames = max([1, total_frames])
        progress_percent = frames_processed * 100.0 / total_frames

        self.progress_bar_control_var.set(progress_percent)

        elapsed_time_seconds = int(time.time() - self.start_time)

        self.frames_applied.configure(text=create_frames_stereo_rectified_text(frames_processed,
                                                                               total_frames,
                                                                               progress_percent))
        self.elapsed_time_label.configure(text=ELAPSED_TIME_PREFIX +
                                               str(datetime.timedelta(seconds=elapsed_time_seconds)))

        if elapsed_time_seconds == 0:
            estimated_time_left_string = ESTIMATED_TIME_LEFT_PREFIX + "Calculating..."
        else:
            estimated_time_left_seconds = int(elapsed_time_seconds / frames_processed * total_frames) - elapsed_time_seconds
            estimated_time_left_string = ESTIMATED_TIME_LEFT_PREFIX + \
                                         str(datetime.timedelta(seconds=estimated_time_left_seconds))
        self.estimated_time_left_label.configure(text=estimated_time_left_string)

    def on_hide_frame(self):
        self.progress_bar.stop()

    def check_thread(self):
        if self.sr_frame_count_thread.is_alive():
            self.master.after(50, self.check_thread)
        else:
            self.progress_bar.stop()
            self.wait_text.configure(text="\nDone!\n\n")
            self.next_button.configure(state=NORMAL)


def create_frames_stereo_rectified_text(frames_processed, total_frames, progress_percent):
    return FRAMES_STEREO_RECTIFIED_PREFIX + str(frames_processed) + "/" + str(total_frames) + \
           " (" + str(round(progress_percent, 2)) + "%)"
