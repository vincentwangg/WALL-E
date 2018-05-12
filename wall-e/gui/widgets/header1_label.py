from tkinter import *


class Header1Label(Label):
    def __init__(self, master, **kw):
        Label.__init__(self, master, font=("futura", 16, "normal"), **kw)
