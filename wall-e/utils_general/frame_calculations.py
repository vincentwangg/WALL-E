# Calculates the following:
#   - First frame to start scanning from for both left and right videos
#   - Last frame to scan for both left and right videos
#   - Total number of frames to scan for each video
def calculate_video_scan_frame_information(first_frame, last_frame_inclusive, left_offset, right_offset,
                                           video_frame_loader):
    first_frame_left = first_frame + left_offset
    first_frame_right = first_frame + right_offset

    if last_frame_inclusive != -1:
        last_frame_left = last_frame_inclusive + left_offset
        last_frame_right = last_frame_inclusive + right_offset
    else:
        last_frame_left = video_frame_loader.last_frame_num_left
        last_frame_right = video_frame_loader.last_frame_num_right

    if last_frame_left > video_frame_loader.last_frame_num_left:
        raise ValueError("Last frame for left video is out of video bounds. Please check inputs.")

    if last_frame_right > video_frame_loader.last_frame_num_right:
        raise ValueError("Last frame for right video is out of video bounds. Please check inputs.")

    num_frames_to_scan = min([last_frame_left - first_frame_left + 1,
                              last_frame_right - first_frame_right + 1])

    return first_frame_left, last_frame_left, first_frame_right, last_frame_right, num_frames_to_scan
