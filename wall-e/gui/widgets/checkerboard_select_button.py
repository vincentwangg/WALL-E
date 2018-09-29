# Button that holds data to use for later
from Tkinter import Button


class CheckerboardSelectButton(Button):
    def __init__(self, master, controller, checkerboard, **kw):
        Button.__init__(self, master, **kw)
        self.master = master
        self.controller = controller
        self.checkerboard = checkerboard
        self.chosen = False

    def choose_checkerboard(self):
      if not self.chosen:
        self.controller.builder.chosen_checkerboard_frames.append(self.checkerboard)
        self.chosen = True
        print "checkerboards chosen length: ", len(self.controller.builder.chosen_checkerboard_frames)
