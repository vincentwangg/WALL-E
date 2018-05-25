import datetime

from gui.abstract_screens.utilities.time_input_util_methods import calculate_frame_num_from_inputs, \
    create_error_message_string, is_frame_range_valid


# All input checks must either return True (if input is valid) or False (if input is not valid).

def frame_input_within_video_bounds_check(time_selection_base_screen):
    frame_num_inputted = calculate_frame_num_from_inputs(time_selection_base_screen)
    left_frame_num = frame_num_inputted + time_selection_base_screen.controller.video_offsets.left_offset
    right_frame_num = frame_num_inputted + time_selection_base_screen.controller.video_offsets.right_offset

    if not time_selection_base_screen.controller.is_frame_num_within_video_bounds(frame_num_inputted):
        error_string = create_error_message_string(frame_num_inputted,
                                                   time_selection_base_screen.controller.video_offsets.left_offset,
                                                   left_frame_num,
                                                   time_selection_base_screen.controller.video_frame_loader.last_frame_num_left,
                                                   time_selection_base_screen.controller.video_offsets.right_offset,
                                                   right_frame_num,
                                                   time_selection_base_screen.controller.video_frame_loader.last_frame_num_right)
        time_selection_base_screen.set_error_message(error_string)
        return False
    return True


def perform_frame_range_chronological_check(first_frame, time_selection_base_screen):
    frame_num_inputted = calculate_frame_num_from_inputs(time_selection_base_screen)

    if not is_frame_range_valid(first_frame, frame_num_inputted):
        error_message_string = "".join([
            "The provided timestamp must be greater than or equal to the provided timestamp earlier.\n",
            "Timestamp provided earlier: ",
            str(datetime.timedelta(seconds=(first_frame / 30))),
            "\nTimestamp provided here: ",
            str(datetime.timedelta(seconds=(frame_num_inputted / 30)))
        ])
        time_selection_base_screen.set_error_message(error_message_string)

        return False
    return True


def sr_scan_frame_range_chronologically_valid_check(time_selection_base_screen):
    first_frame = time_selection_base_screen.controller.sr_scan_frame_range.first_frame

    return perform_frame_range_chronological_check(first_frame, time_selection_base_screen)


def apply_sr_frame_range_chronologically_valid_check(time_selection_base_screen):
    first_frame = time_selection_base_screen.controller.apply_sr_frame_range.first_frame

    return perform_frame_range_chronological_check(first_frame, time_selection_base_screen)


def frame_matching_frame_range_chronologically_valid_check(time_selection_base_screen):
    first_frame = time_selection_base_screen.controller.frame_matching_frame_range.first_frame

    return perform_frame_range_chronological_check(first_frame, time_selection_base_screen)


def frame_matching_frame_range_greater_than_or_equal_to_2(time_selection_base_screen):
    first_frame = time_selection_base_screen.controller.frame_matching_frame_range.first_frame
    last_frame_inclusive_minimum = first_frame + 5 # Arbitrary value to make sure frame matching frame range is valid
    frame_num_inputted = calculate_frame_num_from_inputs(time_selection_base_screen)

    if frame_num_inputted < last_frame_inclusive_minimum:
        error_message_string = "".join([
            "The provided timestamp gives a time range that is too short for frame matching to work properly."
            "\nPlease expand the time range.",
            "\nTimestamp provided earlier: ",
            str(datetime.timedelta(seconds=(first_frame / 30))),
            "\nTimestamp provided here: ",
            str(datetime.timedelta(seconds=(frame_num_inputted / 30)))
        ])
        time_selection_base_screen.set_error_message(error_message_string)

        return False
    return True