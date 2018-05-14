import json
import threading
import time
import datetime
from tkinter import *
from tkinter.ttk import Progressbar
from gui.gui_base_frame import GuiBaseFrame
from gui.pipeline1.constants import *
from gui.widgets.header1_label import Header1Label
from gui.widgets.p_label import PLabel
from stereo_rectification.sr_map_gen import get_list_of_valid_frames_for_sr_tkinter


class SrScanScreen(GuiBaseFrame):
    def __init__(self, parent, controller, **kw):
        GuiBaseFrame.__init__(self, parent, controller, **kw)

    def setup_widgets(self):
        self.content_wrapper = Frame(self)
        self.content_wrapper.configure(bg="white")

        self.screen_title = Header1Label(self.content_wrapper,
                                         text="Finding frames valid for stereo rectification...\n")
        self.progress_bar_control_var = DoubleVar()
        self.progress_bar = Progressbar(self.content_wrapper, orient=HORIZONTAL, mode="determinate",
                                        length=WINDOW_WIDTH / 2, variable=self.progress_bar_control_var)
        self.wait_text = PLabel(self.content_wrapper, text="\nThis might take a few minutes."
                                                           "\nPlease do not change the video files while this is "
                                                           "running.\n")
        self.frames_read_label = PLabel(self.content_wrapper)
        self.valid_frames_found_label = PLabel(self.content_wrapper, text=VALID_FRAMES_FOUND_PREFIX + "0")
        self.elapsed_time_label = PLabel(self.content_wrapper)
        self.estimated_time_left_label = PLabel(self.content_wrapper)
        self.empty_space = PLabel(self.content_wrapper, text=" ")
        self.next_button = Button(self.content_wrapper, text="Next")

        self.screen_title.pack()
        self.progress_bar.pack()
        self.wait_text.pack()
        self.frames_read_label.pack()
        self.valid_frames_found_label.pack()
        self.elapsed_time_label.pack()
        self.estimated_time_left_label.pack()
        self.empty_space.pack()
        self.next_button.pack()
        self.content_wrapper.place(relx=0.5, rely=0.45, anchor=CENTER)

    def start(self):
        self.start_time = time.time()
        self.sr_frame_count_thread = threading.Thread(target=get_list_of_valid_frames_for_sr_tkinter,
                                                      kwargs={"left_offset":
                                                                  self.controller.video_offsets.left_offset,
                                                              "right_offset":
                                                                  self.controller.video_offsets.right_offset,
                                                              "video_frame_loader":
                                                                  self.controller.video_frame_loader,
                                                              "controller":
                                                                  self.controller})
        self.sr_frame_count_thread.start()
        self.master.after(50, self.check_thread)

    def update_frame(self, data):
        progress_data = json.loads(data)

        valid_frames = progress_data[PROGRESS_DICT_VALID_FRAMES_FOUND]
        frames_read = progress_data[PROGRESS_DICT_FRAMES_READ]
        total_frames = progress_data[PROGRESS_DICT_TOTAL_FRAMES]
        progress_percent = frames_read * 100.0 / total_frames

        # Progress values may come in out of order, so if the value that
        # comes in is lower than the current progress, ignore it
        if self.progress_bar.cget("value") < progress_percent:
            self.progress_bar_control_var.set(progress_percent)

        elapsed_time_seconds = int(time.time() - self.start_time)

        self.frames_read_label.configure(text=create_frames_read_text(frames_read, total_frames, progress_percent))
        self.valid_frames_found_label.configure(text=VALID_FRAMES_FOUND_PREFIX + str(valid_frames))
        self.elapsed_time_label.configure(text=ELAPSED_TIME_PREFIX +
                                               str(datetime.timedelta(seconds=elapsed_time_seconds)))

        if elapsed_time_seconds == 0:
            estimated_time_left_string = ESTIMATED_TIME_LEFT_PREFIX + "Calculating..."
        else:
            estimated_time_left_seconds = int(elapsed_time_seconds / frames_read * total_frames) - elapsed_time_seconds
            estimated_time_left_string = ESTIMATED_TIME_LEFT_PREFIX + \
                                         str(datetime.timedelta(seconds=estimated_time_left_seconds))
        self.estimated_time_left_label.configure(text=estimated_time_left_string)

    def stop(self):
        self.progress_bar.stop()

    def check_thread(self):
        if self.sr_frame_count_thread.is_alive():
            self.master.after(50, self.check_thread)
        else:
            self.progress_bar.stop()
            self.wait_text.configure(text="\nDone!\n\n")
            self.next_button.configure(state=NORMAL)


def create_frames_read_text(frames_read, total_frames, progress_percent):
    return FRAMES_READ_PREFIX + str(frames_read) + "/" + str(total_frames) + \
           " (" + str(round(progress_percent, 2)) + "%)"
