from Tkconstants import CENTER

from gui.abstract_screens.abstract_time_selection_base_screen import AbstractTimeSelectionBaseScreen
from gui.pipeline1.utilities.constants import SCREENS_REL_X, SCREENS_REL_Y
from gui.widgets.p_label import PLabel


# To use this class, have the new class inherit this class and add widgets to self.content_wrapper
class AbstractTimeSelectionStartScreen(AbstractTimeSelectionBaseScreen):
    def __init__(self, parent, controller, **kw):
        AbstractTimeSelectionBaseScreen.__init__(self, parent, controller, **kw)

    def init_widgets(self):
        AbstractTimeSelectionBaseScreen.init_widgets(self)

        self.screen_instruction_1_filename_label = PLabel(self.content_wrapper)
        self.screen_instruction_2_label = PLabel(self.content_wrapper)
        self.empty_label_1 = PLabel(self.content_wrapper)

    def add_widgets_to_frame(self):
        self.pack_title_and_instruction_widgets()
        self.empty_label_1.pack()
        self.screen_instruction_1_filename_label.pack()
        self.screen_instruction_2_label.pack()
        self.pack_lower_half_widgets()
        self.content_wrapper.place(relx=SCREENS_REL_X, rely=SCREENS_REL_Y, anchor=CENTER)

    def on_show_frame(self):
        self.set_instruction_1_filename(self.controller.get_filename_of_video_with_0_offset() + "\n")
        self.set_error_message("")

    def update_frame(self, data):
        AbstractTimeSelectionBaseScreen.update_frame(self, data)

    def on_hide_frame(self):
        pass

    def set_input_checks(self):
        AbstractTimeSelectionBaseScreen.set_input_checks(self)

    def on_input_check_success(self):
        AbstractTimeSelectionBaseScreen.on_input_check_success(self)

    def prev_button_command(self):
        AbstractTimeSelectionBaseScreen.prev_button_command(self)

    def next_button_command(self):
        AbstractTimeSelectionBaseScreen.next_button_command(self)

    def set_instruction_1_filename(self, file_of_video_to_open):
        self.screen_instruction_1_filename_label.configure(text=file_of_video_to_open)

    def set_instruction_2_text(self, timestamp_instr_text):
        self.screen_instruction_2_label.configure(text=timestamp_instr_text)
