from Tkinter import Frame, LEFT, Button, CENTER

from gui.pipeline1.utilities.constants import SCREENS_REL_X, SCREEN_REL_Y_45
from gui.widgets.gui_base_frame import GuiBaseFrame
from gui.widgets.header1_label import Header1Label
from gui.widgets.p_label import PLabel


class WelcomeScreen(GuiBaseFrame):
    def __init__(self, parent, controller, **kw):
        GuiBaseFrame.__init__(self, parent, controller, **kw)

    def init_widgets(self):
        self.text_container = Frame(self)
        self.welcome_label = Header1Label(self.text_container,
                                          text="Welcome to the full WALL-E footage processing experience!!")
        self.description_label = PLabel(self.text_container,
                                        text="This process helps you perform the following in order:\n"
                                             "\t1) Frame matching the videos\n"
                                             "\t2) Finding and generating the best SR map\n"
                                             "\t3) Stereo rectifying the videos",
                                        justify=LEFT)
        self.good_luck_label = PLabel(self.text_container, text="Good Luck!")
        self.next_button = Button(self.text_container, text="Get Started",
                                  command=lambda: self.controller.show_next_frame())

    def add_widgets_to_frame(self):
        self.welcome_label.pack()
        self.description_label.pack()
        self.good_luck_label.pack()
        self.next_button.pack()
        self.text_container.place(relx=SCREENS_REL_X, rely=SCREEN_REL_Y_45, anchor=CENTER)

    def on_show_frame(self):
        pass

    def on_hide_frame(self):
        pass
