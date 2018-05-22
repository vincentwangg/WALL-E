from tkinter import CENTER

from gui.pipeline1.constants import SCREENS_REL_X, SCREENS_REL_Y
from gui.pipeline1.utilities.time_selection_base_screen import TimeSelectionBaseScreen


class TimeSelectionEndScreen(TimeSelectionBaseScreen):
    def __init__(self, parent, controller, **kw):
        TimeSelectionBaseScreen.__init__(self, parent, controller, **kw)

    def init_widgets(self):
        super(TimeSelectionEndScreen, self).init_widgets()

    def add_widgets_to_frame(self):
        self.pack_title_and_instruction_widgets()
        self.pack_lower_half_widgets()
        self.content_wrapper.place(relx=SCREENS_REL_X, rely=SCREENS_REL_Y, anchor=CENTER)

    def on_show_frame(self):
        super(TimeSelectionEndScreen, self).on_show_frame()

    def update_frame(self, data):
        super(TimeSelectionEndScreen, self).update_frame(data)

    def on_hide_frame(self):
        pass

    def set_input_checks(self):
        super(TimeSelectionEndScreen, self).set_input_checks()

    def on_input_check_success(self):
        super(TimeSelectionEndScreen, self).on_input_check_success()

    def prev_button_command(self):
        super(TimeSelectionEndScreen, self).prev_button_command()

    def next_button_command(self):
        super(TimeSelectionEndScreen, self).next_button_command()

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
