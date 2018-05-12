from tkinter import *
from gui.gui_base_frame import GuiBaseFrame
from gui.pipeline1.video_selection_screen import VideoSelectionScreen


class WelcomeScreen(GuiBaseFrame):
    def __init__(self, parent, controller):
        GuiBaseFrame.__init__(self, parent, controller)

    def setup_widgets(self):
        self.welcome_label = Label(self, text="Welcome to the full WALL-E footage processing experience!!")
        self.description_label = Label(self,
                                        text="This process helps you perform the following in order:\n"
                                             "\t1) Frame matching the videos\n"
                                             "\t2) Finding and generating the best SR map\n"
                                             "\t3) Stereo rectifying the videos",
                                        justify=LEFT)
        self.good_luck_label = Label(self, text="Good Luck!")
        self.next_button = Button(self, text="Get Started",
                                  command=lambda: self.controller.show_frame(VideoSelectionScreen))

        self.welcome_label.pack()
        self.description_label.pack()
        self.good_luck_label.pack()
        self.next_button.pack()