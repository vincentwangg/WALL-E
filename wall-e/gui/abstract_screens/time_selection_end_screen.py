from Tkinter import CENTER

from gui.abstract_screens.time_selection_base_screen import TimeSelectionBaseScreen
from gui.pipeline1.constants import SCREENS_REL_X, SCREENS_REL_Y


class TimeSelectionEndScreen(TimeSelectionBaseScreen):
    def __init__(self, parent, controller, **kw):
        TimeSelectionBaseScreen.__init__(self, parent, controller, **kw)

    def init_widgets(self):
        TimeSelectionBaseScreen.init_widgets(self)

    def add_widgets_to_frame(self):
        self.pack_title_and_instruction_widgets()
        self.pack_lower_half_widgets()
        self.content_wrapper.place(relx=SCREENS_REL_X, rely=SCREENS_REL_Y, anchor=CENTER)

    def on_show_frame(self):
        TimeSelectionBaseScreen.on_show_frame(self)

    def update_frame(self, data):
        TimeSelectionBaseScreen.update_frame(self, data)

    def on_hide_frame(self):
        pass

    def set_input_checks(self):
        TimeSelectionBaseScreen.set_input_checks(self)

    def on_input_check_success(self):
        TimeSelectionBaseScreen.on_input_check_success(self)

    def prev_button_command(self):
        TimeSelectionBaseScreen.prev_button_command(self)

    def next_button_command(self):
        TimeSelectionBaseScreen.next_button_command(self)

    def pack_title_and_instruction_widgets(self):
        self.screen_title.pack()
        self.screen_instruction_1_label.pack()

    def pack_lower_half_widgets(self):
        self.input_content_wrapper.pack()
        self.error_message_label.pack()
        self.back_button.grid(row=0, column=0)
        self.next_button.grid(row=0, column=1)
        self.button_wrapper.pack()

    # Packs inputs, error message labels, and buttons
    def set_title(self, title):
        self.screen_title.configure(text=title)

    def set_instruction_1_text(self, text):
        self.screen_instruction_1_label.configure(text=text)

    def set_error_message(self, error_message):
        self.error_message_label.configure(text=error_message)
