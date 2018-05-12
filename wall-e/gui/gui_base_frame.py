from tkinter import *


class GuiBaseFrame(Frame):
    def __init__(self, master, controller, **kw):
        Frame.__init__(self, master, **kw)
        self.configure(bg="white")
        self.controller = controller
        self.setup_widgets()

    def setup_widgets(self):
        raise NotImplementedError
