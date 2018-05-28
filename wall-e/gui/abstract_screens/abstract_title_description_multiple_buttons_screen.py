from Tkinter import Frame, Button, CENTER

from gui.pipeline1.utilities.constants import SCREENS_REL_X, SCREEN_REL_Y_47
from gui.widgets.gui_base_frame import GuiBaseFrame
from gui.widgets.header1_label import Header1Label
from gui.widgets.p_label import PLabel


class AbstractTitleDescriptionMultipleButtonsScreen(GuiBaseFrame):
    def __init__(self, parent, controller, title, process_description_message_list,
                 button_text_list, button_command_list, **kw):
        self.screen_title = title
        self.process_description_message_list = process_description_message_list
        self.button_text_list = button_text_list
        self.button_command_list = button_command_list
        GuiBaseFrame.__init__(self, parent, controller, **kw)

    def init_widgets(self):
        self.content_wrapper = Frame(self)

        self.screen_title = Header1Label(self.content_wrapper, text=self.screen_title)
        self.screen_description_label = PLabel(self.content_wrapper,
                                               text=("\n\n".join(self.process_description_message_list)))
        self.button_wrapper = Frame(self.content_wrapper)

        if len(self.button_text_list) != len(self.button_command_list):
            raise ValueError("Button text list and command list must have the same length "
                             "(each text must correspond with a command in both lists).")

        self.buttons = []
        for i in range(0, len(self.button_text_list)):
            self.buttons.append((Button(self.button_wrapper,
                                text=self.button_text_list[i],
                                command=self.button_command_list[i])))

    def add_widgets_to_frame(self):
        self.screen_title.pack()
        self.screen_description_label.pack()
        self.button_wrapper.pack()
        for button in self.buttons:
            button.pack()
        self.content_wrapper.place(relx=SCREENS_REL_X, rely=SCREEN_REL_Y_47, anchor=CENTER)

    def on_show_frame(self):
        pass

    def update_frame(self, data):
        pass

    def on_hide_frame(self):
        pass
