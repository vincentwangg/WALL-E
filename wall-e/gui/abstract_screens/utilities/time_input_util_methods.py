import datetime
from Tkinter import Entry, CENTER

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

    return screen_frame.hour_input, screen_frame.minute_input, screen_frame.seconds_input


def calculate_frame_num_from_inputs(time_selection_base_screen, frames_per_second=30):
    hours = int("0" + time_selection_base_screen.hour_input.get())
    minutes = int("0" + time_selection_base_screen.minute_input.get())
    seconds = int("0" + time_selection_base_screen.seconds_input.get())

    total_seconds = seconds + minutes * 60 + hours * 60 * 60
    frame_num = total_seconds * frames_per_second
    return frame_num


def create_error_message_string(frame_num_inputted,
                                left_offset, left_frame_num, last_frame_num_left,
                                right_offset, right_frame_num, last_frame_num_right):
    frame_num_inputted_str = str(frame_num_inputted)
    text_string = "".join([
        "The provided timestamp is invalid.\nPlease make sure the timestamp is "
        "within the bounds of both videos.\n",
        str(datetime.timedelta(seconds=(frame_num_inputted / 30))),
        " => Frame #",
        frame_num_inputted_str,
        "\nFrame number for left video: ",
        frame_num_inputted_str,
        " + ",
        str(left_offset),
        " (offset) = ",
        str(left_frame_num),
        " (of ",
        str(last_frame_num_left),
        " total)\nFrame number for right video: ",
        frame_num_inputted_str,
        " + ",
        str(right_offset),
        " (offset) = ",
        str(right_frame_num),
        " (of ",
        str(last_frame_num_right),
        " total)"
    ])
    return text_string


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


def is_frame_range_valid(first_frame, last_frame_inclusive):
    if last_frame_inclusive < 0:
        raise ValueError("Last frame inclusive should not be negative. Please prevent negative frame inputs")

    return first_frame <= last_frame_inclusive
