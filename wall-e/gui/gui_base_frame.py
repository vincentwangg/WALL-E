from tkinter import *


class GuiBaseFrame(Frame):
    def __init__(self, master, controller, **kw):
        Frame.__init__(self, master, borderwidth=2, relief="groove", **kw)
        self.controller = controller
        self.setup_widgets()

    def setup_widgets(self):
        raise NotImplementedError

    def set_dimensions(self, width, height):
        self.configure(width=width, height=height)
