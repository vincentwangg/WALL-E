from Tkinter import Label


class Header1Label(Label):
    def __init__(self, master, **kw):
        Label.__init__(self, master, font=("futura", 16, "normal"), **kw)
