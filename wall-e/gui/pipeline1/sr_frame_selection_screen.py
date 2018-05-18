from tkinter import Canvas, Frame, Scrollbar, Label, VERTICAL, CENTER, Button

from gui.gui_base_frame import GuiBaseFrame
from gui.pipeline1.constants import WINDOW_WIDTH, WINDOW_HEIGHT, SCREENS_REL_X, SCREENS_REL_Y
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
        self.canvas = Canvas(self.canvas_wrapper, width=int(WINDOW_WIDTH * 3 / 4), height=(WINDOW_HEIGHT * 2 / 3),
                             scrollregion=(0, 0, int(WINDOW_WIDTH * 3 / 4), (WINDOW_HEIGHT * 2 / 3)))
        self.scroll_bar = Scrollbar(self.canvas_wrapper, orient=VERTICAL, command=self.canvas.yview)
        self.results_list_frame = Frame(self.canvas)

        self.canvas.configure(yscrollcommand=self.scroll_bar.set)
        self.canvas.create_window(0, 0, window=self.results_list_frame)
        self.canvas.bind_all("<Up>", self.on_up_key)
        self.canvas.bind_all("<Down>", self.on_down_key)

        for row in range(100):
            Label(self.results_list_frame, text="%s" % row, width=3, borderwidth="1",
                     relief="solid").grid(row=row, column=0)
            t = "this is the second column for row %s" % row
            Label(self.results_list_frame, text=t).grid(row=row, column=1)

        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scroll_bar.grid(row=0, column=1, sticky="ns")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.screen_title.pack()
        self.screen_description.pack()
        self.canvas_wrapper.pack()
        self.content_wrapper.place(relx=SCREENS_REL_X, rely=0.48, anchor=CENTER)

    def start(self):
        self.master.update()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def update_frame(self, data):
        pass

    def stop(self):
        pass

    def on_up_key(self, event):
        self.canvas.yview_scroll(-1, 'units')

    def on_down_key(self, event):
        self.canvas.yview_scroll(1, 'units')