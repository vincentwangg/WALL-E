from Tkconstants import CENTER

from gui.abstract_screens.time_selection_base_screen import TimeSelectionBaseScreen
from gui.pipeline1.constants import SCREENS_REL_X, SCREENS_REL_Y
from gui.widgets.p_label import PLabel


# To use this class, have the new class inherit this class and add widgets to self.content_wrapper
class TimeSelectionStartScreen(TimeSelectionBaseScreen):
    def __init__(self, parent, controller, **kw):
        TimeSelectionBaseScreen.__init__(self, parent, controller, **kw)

    def init_widgets(self):
        TimeSelectionBaseScreen.init_widgets(self)

        self.screen_instruction_1_filename_label = PLabel(self.content_wrapper)
        self.screen_instruction_2_label = PLabel(self.content_wrapper)

    def add_widgets_to_frame(self):
        self.pack_title_and_instruction_widgets()
        self.screen_instruction_1_filename_label.pack()
        self.screen_instruction_2_label.pack()
        self.pack_lower_half_widgets()
        self.content_wrapper.place(relx=SCREENS_REL_X, rely=SCREENS_REL_Y, anchor=CENTER)

    def on_show_frame(self):
        TimeSelectionBaseScreen.on_show_frame(self)

    def update_frame(self, data):
        TimeSelectionBaseScreen.update_frame(self, data)

    def on_hide_frame(self):
        TimeSelectionBaseScreen.on_hide_frame(self)

    def set_input_checks(self):
        TimeSelectionBaseScreen.set_input_checks(self)

    def on_input_check_success(self):
        TimeSelectionBaseScreen.on_input_check_success(self)

    def prev_button_command(self):
        TimeSelectionBaseScreen.prev_button_command(self)

    def next_button_command(self):
        TimeSelectionBaseScreen.next_button_command(self)

    def set_instruction_1_filename(self, file_of_video_to_open):
        self.screen_instruction_1_filename_label.configure(text=file_of_video_to_open)

    def set_instruction_2_text(self, timestamp_instr_text):
        self.screen_instruction_2_label.configure(text=timestamp_instr_text)
