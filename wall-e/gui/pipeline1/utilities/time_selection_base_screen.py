from tkinter import Frame, Button

from gui.pipeline1.utilities.inputs import setup_hms_input
from gui.widgets.gui_base_frame import GuiBaseFrame
from gui.widgets.header1_label import Header1Label
from gui.widgets.p_label import PLabel


class TimeSelectionBaseScreen(GuiBaseFrame):
    def __init__(self, parent, controller, **kw):
        GuiBaseFrame.__init__(self, parent, controller, **kw)
        self.input_checks = []
        self.set_input_checks()

    def init_widgets(self):
        self.content_wrapper = Frame(self)

        self.screen_title = Header1Label(self.content_wrapper)
        self.screen_instruction_1_label = PLabel(self.content_wrapper)

        self.input_content_wrapper = Frame(self.content_wrapper)
        self.hour_input, self.minute_input, self.seconds_input = setup_hms_input(self, self.input_content_wrapper)
        self.error_message_label = PLabel(self.content_wrapper, fg="red")

        self.button_wrapper = Frame(self.content_wrapper)
        self.back_button = Button(self.button_wrapper, text="Back",
                                  command=lambda: self.prev_button_command())
        self.next_button = Button(self.button_wrapper, text="Next",
                                  command=lambda: self.next_button_command())

    def add_widgets_to_frame(self):
        super(TimeSelectionBaseScreen, self).add_widgets_to_frame()

    def on_show_frame(self):
        super(TimeSelectionBaseScreen, self).on_show_frame()

    def update_frame(self, data):
        super(TimeSelectionBaseScreen, self).update_frame(data)

    def on_hide_frame(self):
        super(TimeSelectionBaseScreen, self).on_hide_frame()

    def set_input_checks(self):
        raise NotImplementedError

    def on_input_check_success(self):
        raise NotImplementedError

    def next_button_command(self):
        if self.perform_input_checks():
            self.set_error_message("")
            self.on_input_check_success()
            self.controller.show_next_frame()

    def prev_button_command(self):
        self.controller.show_prev_frame()

    def perform_input_checks(self):
        for input_check in self.input_checks:
            if not input_check(self):
                return False
        return True

    def pack_title_and_instruction_widgets(self):
        self.screen_title.pack()
        self.screen_instruction_1_label.pack()

    # Packs inputs, error message labels, and buttons
    def pack_lower_half_widgets(self):
        self.input_content_wrapper.pack()
        self.error_message_label.pack()
        self.back_button.grid(row=0, column=0)
        self.next_button.grid(row=0, column=1)
        self.button_wrapper.pack()

    def set_title(self, title):
        self.screen_title.configure(text=title)

    def set_instruction_1_text(self, text):
        self.screen_instruction_1_label.configure(text=text)

    def set_error_message(self, error_message):
        self.error_message_label.configure(text=error_message)

    def add_input_check(self, input_check_lambda):
        self.input_checks.append(input_check_lambda)
