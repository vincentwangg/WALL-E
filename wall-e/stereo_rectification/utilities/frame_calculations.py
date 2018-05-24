def calculate_last_frame_and_num_frames_to_scan(first_frame, last_frame_inclusive, left_offset, right_offset,
                                                video_frame_loader):
    first_frame_left = first_frame + left_offset
    first_frame_right = first_frame + right_offset

    if last_frame_inclusive != -1:
        last_frame_left = last_frame_inclusive + left_offset
        last_frame_right = last_frame_inclusive + right_offset
    else:
        last_frame_left = video_frame_loader.last_frame_num_left
        last_frame_right = video_frame_loader.last_frame_num_right

    num_frames_to_scan = min([last_frame_left - first_frame_left,
                              last_frame_right - first_frame_right])

    if num_frames_to_scan == 0:
        num_frames_to_scan = 1

    return last_frame_left, last_frame_right, num_frames_to_scan
