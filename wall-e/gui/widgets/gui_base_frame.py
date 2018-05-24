from Tkinter import Frame


class GuiBaseFrame(Frame):
    def __init__(self, master, controller, **kw):
        Frame.__init__(self, master, **kw)
        self.master = master
        self.controller = controller
        self.init_widgets()
        self.add_widgets_to_frame()

    def init_widgets(self):
        raise NotImplementedError

    def add_widgets_to_frame(self):
        raise NotImplementedError

    # Perform any logic needed when the frame is on top
    def on_show_frame(self):
        raise NotImplementedError

    # Main use is for progress bars being updated.
    def update_frame(self, data):
        raise NotImplementedError

    # Perform any logic needed when frame is no longer in focus
    def on_hide_frame(self):
        raise NotImplementedError

    def set_dimensions(self, width, height):
        self.configure(width=width, height=height)
