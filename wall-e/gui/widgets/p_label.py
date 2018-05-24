from Tkinter import Label


class PLabel(Label):
    def __init__(self, master, **kw):
        Label.__init__(self, master, font=("quicksand", 14, "normal"), **kw)
