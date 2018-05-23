import datetime
import threading
import time
from tkinter import Frame, DoubleVar, HORIZONTAL, Button, DISABLED, CENTER, NORMAL
from tkinter.ttk import Progressbar

from gui.pipeline1.constants import WINDOW_WIDTH, SCREENS_REL_X, SCREENS_REL_Y
from gui.utilities.constants import PROGRESS_SCREEN_PERCENT_DONE, PROGRESS_SCREEN_MESSAGE_LIST, ELAPSED_TIME_PREFIX, \
    ESTIMATED_TIME_LEFT_PREFIX
from gui.widgets.gui_base_frame import GuiBaseFrame
from gui.widgets.header1_label import Header1Label
from gui.widgets.p_label import PLabel

THREAD_CHECK_ALIVE_INTERVAL_MS = 50


class ProgressScreen(GuiBaseFrame):
    # Backend logic thread should be making calls to controller.update_frame() to update the UI while logic runs.
    def __init__(self, parent, controller, backend_logic_function, **kw):
        GuiBaseFrame.__init__(self, parent, controller, **kw)
        self.backend_logic_function = backend_logic_function

    def init_widgets(self):
        self.content_wrapper = Frame(self)
        self.content_wrapper.configure(bg="white")

        self.screen_title = Header1Label(self.content_wrapper)
        self.empty_space_1 = PLabel(self.content_wrapper)
        self.progress_bar_control_var = DoubleVar()
        self.progress_bar = Progressbar(self.content_wrapper, orient=HORIZONTAL, mode="determinate",
                                        length=WINDOW_WIDTH / 2, variable=self.progress_bar_control_var)
        self.wait_text = PLabel(self.content_wrapper, text="\nThis might take a few minutes."
                                                           "\nPlease do not change the video files while this is "
                                                           "running.\n")
        self.information_display = PLabel(self.content_wrapper)
        self.empty_space_2 = PLabel(self.content_wrapper)
        self.next_button = Button(self.content_wrapper, text="Next", state=DISABLED,
                                  command=lambda: self.controller.show_next_frame())

    def add_widgets_to_frame(self):
        self.screen_title.pack()
        self.empty_space_1.pack()
        self.progress_bar.pack()
        self.wait_text.pack()
        self.information_display.pack()
        self.empty_space_2.pack()
        self.next_button.pack()
        self.content_wrapper.place(relx=SCREENS_REL_X, rely=SCREENS_REL_Y, anchor=CENTER)

    def on_show_frame(self):
        self.start_time = time.time()
        self.backend_logic_thread = threading.Thread(target=self.backend_logic_function,
                                                kwargs={"controller": self.controller})
        self.backend_logic_thread.start()
        self.master.after(THREAD_CHECK_ALIVE_INTERVAL_MS, self.check_thread)

    # Data should be a dictionary with keys "percent_done" and "message_list".
    def update_frame(self, data):
        percent_done = data[PROGRESS_SCREEN_PERCENT_DONE]
        message_list = data[PROGRESS_SCREEN_MESSAGE_LIST]

        self.progress_bar_control_var.set(percent_done)

        elapsed_time_seconds = int(time.time() - self.start_time)
        elapsed_time_message = ELAPSED_TIME_PREFIX + str(datetime.timedelta(seconds=elapsed_time_seconds))

        if elapsed_time_seconds == 0:
            estimated_time_left_string = ESTIMATED_TIME_LEFT_PREFIX + "Calculating..."
        else:
            estimated_time_left_seconds = int(elapsed_time_seconds / percent_done * 100.0) - elapsed_time_seconds
            estimated_time_left_string = ESTIMATED_TIME_LEFT_PREFIX + \
                                         str(datetime.timedelta(seconds=estimated_time_left_seconds))

        message_list.append(elapsed_time_message)
        message_list.append(estimated_time_left_string)

        self.set_information_display_text(message_list)

    def on_hide_frame(self):
        self.progress_bar.stop()

    def set_title(self, title):
        self.screen_title.configure(text=title)

    def set_information_display_text(self, message_list):
        self.information_display.configure(text=("\n".join(message_list)))

    def check_thread(self):
        if self.backend_logic_thread.is_alive():
            self.master.after(THREAD_CHECK_ALIVE_INTERVAL_MS, self.check_thread)
        else:
            self.progress_bar.stop()
            self.wait_text.configure(text="\nDone!\n\n")
            self.next_button.configure(state=NORMAL)
