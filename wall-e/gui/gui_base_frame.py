from tkinter import *


class GuiBaseFrame(Frame):
    def __init__(self, master, controller, **kw):
        Frame.__init__(self, master, **kw)
        self.controller = controller
        self.setup_widgets()

    def setup_widgets(self):
        raise NotImplementedError

    def set_dimensions(self, width, height):
        self.configure(width=width, height=height)

    # Perform any logic needed when the frame is on top
    def start(self):
        raise NotImplementedError

    # Main use is for progress bars being updated.
    def update_frame(self, data):
        raise NotImplementedError

    # Perform any logic needed when frame is no longer in focus
    def stop(self):
        raise NotImplementedError
