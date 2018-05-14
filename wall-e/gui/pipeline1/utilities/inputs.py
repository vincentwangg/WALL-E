from tkinter import *
from gui.widgets.p_label import PLabel

ENTRY_WIDTH = 5
INSERT_ACTION = "1"


def setup_hms_input(screen_frame, input_content_wrapper):
    validate_command = (screen_frame.register(validate_hms_input), "%d", "%S")

    screen_frame.hour_label = PLabel(input_content_wrapper, text="H: ")
    screen_frame.hour_input = Entry(input_content_wrapper, width=ENTRY_WIDTH, justify=CENTER,
                                    validate="key", validatecommand=validate_command)
    screen_frame.hour_input.insert(0, 0)
    screen_frame.hour_label.grid(row=0, column=0)
    screen_frame.hour_input.grid(row=0, column=1)

    screen_frame.minute_label = PLabel(input_content_wrapper, text="M: ")
    screen_frame.minute_input = Entry(input_content_wrapper, width=ENTRY_WIDTH, justify=CENTER,
                                    validate="key", validatecommand=validate_command)
    screen_frame.minute_input.insert(0, 0)
    screen_frame.minute_label.grid(row=0, column=2)
    screen_frame.minute_input.grid(row=0, column=3)

    screen_frame.seconds_label = PLabel(input_content_wrapper, text="S: ")
    screen_frame.seconds_input = Entry(input_content_wrapper, width=ENTRY_WIDTH, justify=CENTER,
                                    validate="key", validatecommand=validate_command)
    screen_frame.seconds_input.insert(0, 0)
    screen_frame.seconds_label.grid(row=0, column=4)
    screen_frame.seconds_input.grid(row=0, column=5)


def validate_hms_input(action, text):
    if action == INSERT_ACTION and not is_value_int(text):
        return False
    else:
        return True


def is_value_int(value_if_allowed):
    try:
        int(value_if_allowed)
    except ValueError:
        return False
    return True
