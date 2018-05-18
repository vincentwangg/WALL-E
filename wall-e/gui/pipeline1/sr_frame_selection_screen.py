from tkinter import Canvas, Frame, Scrollbar, Label, VERTICAL, CENTER, Button

import datetime

from gui.gui_base_frame import GuiBaseFrame
from gui.pipeline1.constants import WINDOW_WIDTH, WINDOW_HEIGHT, SCREENS_REL_X, SCREENS_REL_Y, LEFT, RIGHT, \
    VIDEO_SR_SELECT_PREVIEW_WIDTH, VIDEO_SR_SELECT_PREVIEW_HEIGHT, FRAME_NUM_LABEL
from gui.widgets.header1_label import Header1Label
from gui.widgets.p_label import PLabel


class SrFrameSelection(GuiBaseFrame):
    def __init__(self, parent, controller, **kw):
        GuiBaseFrame.__init__(self, parent, controller, **kw)

    def setup_widgets(self):
        self.content_wrapper = Frame(self)
        self.screen_title = Header1Label(self.content_wrapper, text="Stereo Rectification Frame Selection")
        self.screen_description = PLabel(self.content_wrapper, text="Please select a frame that has a satisfactory "
                                                                    "stereo rectification result.")

        self.canvas_wrapper = Frame(self.content_wrapper, borderwidth="1", relief="solid")
        self.canvas = Canvas(self.canvas_wrapper, width=int(WINDOW_WIDTH * 7 / 8), height=(WINDOW_HEIGHT * 2 / 3))
        self.scroll_bar = Scrollbar(self.canvas_wrapper, orient=VERTICAL, command=self.canvas.yview)
        self.results_list_frame = Frame(self.canvas)

        self.canvas.configure(yscrollcommand=self.scroll_bar.set)
        self.canvas.create_window(VIDEO_SR_SELECT_PREVIEW_WIDTH, VIDEO_SR_SELECT_PREVIEW_HEIGHT,
                                  window=self.results_list_frame)
        self.canvas.bind_all("<Up>", self.on_up_key)
        self.canvas.bind_all("<Down>", self.on_down_key)

        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scroll_bar.grid(row=0, column=1, sticky="ns")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.screen_title.grid(row=0)
        self.screen_description.grid(row=1)
        self.canvas_wrapper.grid(row=2, sticky="nsew")
        self.content_wrapper.place(relx=SCREENS_REL_X, rely=0.48, anchor=CENTER)

    def start(self):
        for row in range(0, len(self.controller.sr_results)):
            frame_num = self.controller.sr_results[row][FRAME_NUM_LABEL]

            result_entry = Frame(self.results_list_frame, borderwidth="1", relief="solid")
            description = PLabel(result_entry, text="Frame #" + str(int(frame_num)) +
                                                    ", Time: " +
                                                    str(datetime.timedelta(seconds=frame_num / 30)))
            preview_wrapper = Frame(result_entry)
            left_video_preview = Label(preview_wrapper, image=self.controller.sr_results[row][LEFT])
            right_video_preview = Label(preview_wrapper, image=self.controller.sr_results[row][RIGHT])
            select_button = Button(preview_wrapper, text="Select")

            description.pack()
            left_video_preview.grid(row=row, column=0)
            right_video_preview.grid(row=row, column=1)
            select_button.grid(row=row, column=2)
            preview_wrapper.pack()
            result_entry.pack()

        self.master.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.canvas.yview_moveto(0)

    def update_frame(self, data):
        pass

    def stop(self):
        pass

    def on_up_key(self, event):
        self.canvas.yview_scroll(-5, 'units')

    def on_down_key(self, event):
        self.canvas.yview_scroll(5, 'units')