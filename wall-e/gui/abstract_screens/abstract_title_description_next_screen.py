from Tkinter import Frame, Button, CENTER

from gui.pipeline1.utilities.constants import SCREENS_REL_X, SCREEN_REL_Y_45
from gui.widgets.gui_base_frame import GuiBaseFrame
from gui.widgets.header1_label import Header1Label
from gui.widgets.p_label import PLabel


class AbstractTitleDescriptionNextScreen(GuiBaseFrame):
    def __init__(self, parent, controller, title, process_description_message_list, **kw):
        self.screen_title = title
        self.process_description_message_list = process_description_message_list
        GuiBaseFrame.__init__(self, parent, controller, **kw)

    def init_widgets(self):
        self.content_wrapper = Frame(self)

        self.screen_title = Header1Label(self.content_wrapper, text=self.screen_title)
        self.screen_description_label = PLabel(self.content_wrapper,
                                               text=("\n\n".join(self.process_description_message_list)))
        self.button_wrapper = Frame(self.content_wrapper)
        self.next_button = Button(self.button_wrapper, text="Next",
                                  command=lambda: self.on_next_button())

    def add_widgets_to_frame(self):
        self.screen_title.pack()
        self.screen_description_label.pack()
        self.button_wrapper.pack()
        self.next_button.pack()
        self.content_wrapper.place(relx=SCREENS_REL_X, rely=SCREEN_REL_Y_45, anchor=CENTER)

    def on_show_frame(self):
        pass

    def update_frame(self, data):
        pass

    def on_hide_frame(self):
        pass

    def on_next_button(self):
        raise NotImplementedError
