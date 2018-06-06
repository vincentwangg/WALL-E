"""
Contains functions to generate a stereo rectification map.

Some functions that generate an SR map may be similar to each other because there is a command line and
GUI backend version of the same operation. However, the GUI backend version of the code is more updated
and will most likely work better than the command line version.

Stereo rectification code imported from the following link:
https://medium.com/@kennethjiang/calibrate-fisheye-lens-using-opencv-part-2-13990f1b157f
"""

import argparse

from config.keycode_setup import *
from gui.abstract_screens.utilities.constants import PROGRESS_SCREEN_PERCENT_DONE, PROGRESS_SCREEN_MESSAGE_LIST
from gui.pipeline1.utilities.constants import FRAME_NUM_LABEL, FRAMES_READ_PREFIX, \
    VALID_FRAMES_FOUND_PREFIX
from stereo_rectification.constants import SR_COLLECTING_SAMPLES, SR_CALCULATING_MAP, SR_FINISHED_CALCULATING, SR_FAILED
from stereo_rectification.grayscale_converter import convert_to_gray
from stereo_rectification.sr_map import SR_MAP_FILENAME, SrMap
from utils_general.file_checker import check_if_file_exists
from utils_general.frame_calculations import calculate_video_scan_frame_information
from utils_general.video_frame_loader import VideoFrameLoader

# You should replace these 3 lines with the output in calibration step (calibrate.py)
CHECKERBOARD = (8, 6)
DIM = (640, 478)  # deinterlaced video is now 640 X 478
K = np.array(
    [[526.756924435422, 0.0, 330.221556181272], [0.0, 478.43311043812145, 249.44524334088075], [0.0, 0.0, 1.0]])
D = np.array([[-0.07527166402108293], [0.006777363197177597], [-0.32231954249568173], [0.43735394851622683]])

map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_32F)

SR_MAP_GENERATED_MESSAGE = "\nA file named \"" + SR_MAP_FILENAME + "\" has been generated with the SR " \
                                                                   "map!\nFor future use, this file is " \
                                                                   "recommended to be copied somewhere and " \
                                                                   "renamed. "

# GUI METHODS START #


# For GUI class VideoScanScreen in sr_scan_progress_screen.py
def scan_video_and_build_sr_map_gui(controller):
    """
    GUI backend function for collecting frames valid for SR and building an SR map.

    The video is scanned through for frames that have a chessboard in view and uses
    that information to build a final SR map for the stereo footage.

    The GUI is updated regularly to show progress and the SR map is sent to the
    controller once the map is generated.

    :param controller: GUI controller
    """
    sr_results = []

    first_frame = controller.sr_scan_frame_range.first_frame
    last_frame_inclusive = controller.sr_scan_frame_range.last_frame_inclusive
    left_offset = controller.video_offsets.left_offset
    right_offset = controller.video_offsets.right_offset
    video_frame_loader = controller.video_frame_loader

    first_frame_left, last_frame_left, first_frame_right, last_frame_right, num_frames_to_scan = \
        calculate_video_scan_frame_information(
            first_frame,
            last_frame_inclusive,
            left_offset,
            right_offset,
            video_frame_loader)

    video_frame_loader.set_left_current_frame_num(first_frame_left)
    video_frame_loader.set_right_current_frame_num(first_frame_right)

    num_frames_scanned = 0
    objpoints = []
    img_points_left = []
    img_points_right = []

    update_sr_progress_ui(controller, len(sr_results), num_frames_scanned, num_frames_to_scan,
                          SR_COLLECTING_SAMPLES)

    while True:
        left_frame_num = video_frame_loader.get_left_current_frame_num()
        right_frame_num = video_frame_loader.get_right_current_frame_num()

        # If one of the videos reach their last frame to scan
        if left_frame_num > last_frame_left or right_frame_num > last_frame_right:
            break

        l_success, left_img = video_frame_loader.get_next_left_frame()
        r_success, right_img = video_frame_loader.get_next_right_frame()

        # If one of the videos reach the end of video
        if not l_success or not r_success:
            break

        if is_valid_sr_frame(left_img, right_img):
            img_left_undistorted = convert_to_gray(undistort(left_img))
            img_right_undistorted = convert_to_gray(undistort(right_img))
            success = add_obj_point(img_left_undistorted, img_right_undistorted,
                                    objpoints, img_points_left, img_points_right)
            if success:
                sr_results.append({FRAME_NUM_LABEL: min([left_frame_num, right_frame_num])})

        num_frames_scanned += 1

        if num_frames_scanned % 10 == 0:
            update_sr_progress_ui(controller, len(sr_results), num_frames_scanned, num_frames_to_scan,
                                  SR_COLLECTING_SAMPLES)

    update_sr_progress_ui(controller, len(sr_results), num_frames_scanned, num_frames_to_scan, SR_CALCULATING_MAP)

    if len(sr_results) > 0:
        controller.sr_map = generate_sr_map_from_obj_and_img_points(objpoints, img_points_left, img_points_right)
    else:
        update_sr_progress_ui(controller, len(sr_results), num_frames_scanned, num_frames_to_scan,
                              SR_FAILED, sr_map_phase_finished=True)
        return

    controller.sr_results = sr_results
    update_sr_progress_ui(controller, len(sr_results), num_frames_scanned, num_frames_to_scan,
                          SR_FINISHED_CALCULATING, sr_map_phase_finished=True)


def add_obj_point(left_img, right_img, objpoints, img_points_left, img_points_right):
    """
    Helper function to the main GUI backend function, scan_video_and_build_sr_map_gui(). Adds object and image points
    to their corresponding lists for SR map generation.

    If the provided left and right images both contain a chessboard in the view of the frame, then the object
    point and image points for that frame is added to their corresponding lists.

    :param left_img: Left image frame
    :param right_img: Right image frame
    :param objpoints: List of object points
    :param img_points_left: List of left image points
    :param img_points_right: List of right image points
    :return: Whether or not the object point and image points were successfully added to their lists
    """

    img_left_corners_success, img_right_corners_success, img_left_corner_coords, img_right_corner_coords = \
        find_chessboard_corners(left_img, right_img)

    if not (img_left_corners_success and img_right_corners_success):
        return False

    # Tuning these parameters does not appear to effect the end result
    max_iterations = 30
    epsilon = 0.0001
    criteria = (cv2.TERM_CRITERIA_MAX_ITER + cv2.TERM_CRITERIA_EPS, max_iterations, epsilon)

    # Create (x,y,z) object points for all intersections on checkerboard grid
    objp = np.zeros((CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)

    # If found, add object points to objpoints array, and add image points (after refining them) to imgpoints array
    if img_left_corners_success and img_right_corners_success:
        objpoints.append(objp)

        # cornerSubPix refines the corner coordinates. (tuning these params does nothing)
        img_points_left.append(cv2.cornerSubPix(left_img, img_left_corner_coords, (11, 11), (-1, -1), criteria))
        img_points_right.append(cv2.cornerSubPix(right_img, img_right_corner_coords, (11, 11), (-1, -1), criteria))

    return True


def generate_sr_map_from_obj_and_img_points(objpoints, img_points_left, img_points_right):
    """Generates an SR map from the list of object and image points."""

    reprojection_error_left, cam_mtx_l, dist_l, rotation_vec_left, translation_vec_left = cv2.calibrateCamera(
        objpoints,
        img_points_left,
        DIM,
        None, None)
    reprojection_error_right, cam_mtx_r, dist_r, rotation_vec_right, translation_vec_right = cv2.calibrateCamera(
        objpoints,
        img_points_right,
        DIM,
        None, None)

    # getting optimal camera matrix and setting alpha to 0
    alpha = 0.9
    cam_mtx_l, _ = cv2.getOptimalNewCameraMatrix(cam_mtx_l, dist_l, DIM, alpha)
    cam_mtx_r, _ = cv2.getOptimalNewCameraMatrix(cam_mtx_r, dist_r, DIM, alpha)

    # https://docs.opencv.org/3.1.0/d9/d0c/group__calib3d.html#ga246253dcc6de2e0376c599e7d692303a
    img_left_corners_success, cam_mtx_l, dist_l, cam_mtx_r, dist_r, R, T, E, F = cv2.stereoCalibrate(
        objpoints,
        img_points_left,
        img_points_right,
        cam_mtx_l, dist_l, cam_mtx_r, dist_r,
        DIM,
        flags=cv2.CALIB_SAME_FOCAL_LENGTH + cv2.CALIB_FIX_FOCAL_LENGTH + cv2.CALIB_ZERO_TANGENT_DIST)
    # cv2.CALIB_USE_INTRINSIC_GUESS

    # stereo rectify
    R1, R2, P1, P2, Q, validPixROI1, validPixROI2 = cv2.stereoRectify(cam_mtx_l,
                                                                      dist_l,
                                                                      cam_mtx_r,
                                                                      dist_r,
                                                                      DIM,
                                                                      R, T, alpha=alpha)

    return SrMap(cam_mtx_l, dist_l, R1, P1, cam_mtx_r, dist_r, R2, P2)


def update_sr_progress_ui(controller, valid_frames, num_frames_scanned, num_frames_to_scan,
                          sr_map_calculation_message, sr_map_phase_finished=False):
    """Updates the stereo rectification map generation UI progress screen through the GUI controller."""
    progress_percent = num_frames_scanned * 100.0 / num_frames_to_scan * 0.8
    if sr_map_phase_finished:
        progress_percent += 20.0

    frames_processed_message = create_frames_read_text(num_frames_scanned, num_frames_to_scan, progress_percent)
    valid_frames_found_message = VALID_FRAMES_FOUND_PREFIX + str(valid_frames)
    controller.update_frame({
        PROGRESS_SCREEN_PERCENT_DONE: progress_percent,
        PROGRESS_SCREEN_MESSAGE_LIST: [
            frames_processed_message,
            valid_frames_found_message,
            sr_map_calculation_message
        ]
    })


def create_frames_read_text(frames_read, total_frames, progress_percent):
    """Helper function to create the message in the UI that shows how many frames have been read."""
    return FRAMES_READ_PREFIX + str(frames_read) + "/" + str(total_frames) + \
           " (" + str(round(progress_percent, 2)) + "%)"


# GUI METHODS END #


def find_and_generate_best_sr_map(left_video_filename, right_video_filename,
                                  left_offset=0, right_offset=0,
                                  first_frame=0, show_original_frame=False, show_undistorted_frame=False):
    """
    Walks the user through the process in command line for finding and generating the best SR map

    It's preferred that the GUI version of this method is used as this function is not as updated and
    prone to more errors. Basically, try to use the GUI whenever possible.
    """
    print("Welcome to the Stereo Rectification (SR) Map Generator!")
    print("\nThere will be 2 steps to finding the best frame to use to get the best SR map:")
    print("\t1) Go through the video and accept frames that, in your opinion, will work well")
    print("\t2) Go through the frames you've already selected and choose the frame you think works best")
    print("\nGood luck!")
    print("\nFinding the first frame valid for SR map generation...")

    video_frame_loader = VideoFrameLoader(left_video_filename, right_video_filename)

    frame_num = first_frame
    frames = find_valid_frames_for_sr(frame_num, left_offset, right_offset, show_original_frame, show_undistorted_frame,
                                      video_frame_loader)

    if len(frames) == 0:
        print("\nNo frames selected for SR map generation. Exiting now.")
        sys.exit(0)
    elif len(frames) == 1:
        vc_obj_left_success, img_left = video_frame_loader.get_left_frame(frames[0] + left_offset)
        vc_obj_right_success, img_right = video_frame_loader.get_right_frame(frames[0] + right_offset)

        if not vc_obj_left_success or not vc_obj_right_success:
            sys.exit("Frame could not be read from video, this shouldn't happen.")

        img_left_undistorted = convert_to_gray(undistort(img_left))
        img_right_undistorted = convert_to_gray(undistort(img_right))

        while True:
            valid_sr_frame, img_left_sr, img_right_sr, _ = \
                generate_sr_map(img_left_undistorted, img_right_undistorted)
            show_sr_images(valid_sr_frame, img_left_sr, img_right_sr)

            print("\nOnly 1 frame selected for SR map generation.")
            print("Please review the window and press Y/N")
            print("to accept/reject the frame to generate the SR map.")
            key = cv2.waitKey(0)
            cv2.destroyAllWindows()
            cv2.waitKey(1)

            if key == get_keycode_from_key_code_entry(Y_KEY):
                print(SR_MAP_GENERATED_MESSAGE)
                return
            elif key == get_keycode_from_key_code_entry(N_KEY):
                display_no_frames_left_message(frames)
    else:
        final_frame = select_final_frame_from_multiple_frames(frames,
                                                              video_frame_loader=video_frame_loader,
                                                              left_offset=left_offset,
                                                              right_offset=right_offset)

        vc_obj_left_success, img_left = video_frame_loader.get_left_frame(final_frame + left_offset)
        vc_obj_right_success, img_right = video_frame_loader.get_right_frame(final_frame + right_offset)

        if not vc_obj_left_success or not vc_obj_right_success:
            sys.exit("Frame could not be read from video, this shouldn't happen.")

        img_left_undistorted = convert_to_gray(undistort(img_left))
        img_right_undistorted = convert_to_gray(undistort(img_right))

        generate_sr_map(img_left_undistorted, img_right_undistorted)


def find_valid_frames_for_sr(frame_num, left_offset, right_offset, show_original_frame, show_undistorted_frame,
                             video_frame_loader):
    """Helper function for walking the user through the command line step where the user can choose
    to use the currently displayed SR map."""
    frames = []

    while True:
        vc_obj_left_success, img_left = video_frame_loader.get_left_frame(frame_num + left_offset)
        vc_obj_right_success, img_right = video_frame_loader.get_right_frame(frame_num + right_offset)

        if not vc_obj_left_success or not vc_obj_right_success:
            print("Reached the end of video")
            sys.exit(0)

        img_left_undistorted = convert_to_gray(undistort(img_left))
        img_right_undistorted = convert_to_gray(undistort(img_right))

        while True:
            valid_frame_found, left_img_sr, right_img_sr, sr_map = \
                generate_sr_map(img_left_undistorted, img_right_undistorted)
            if valid_frame_found:
                if show_original_frame:
                    cv2.imshow("Original Left", img_left)
                    cv2.imshow("Original Right", img_right)
                if show_undistorted_frame:
                    cv2.imshow("Left Undistorted", img_left_undistorted)
                    cv2.imshow("Right Undistorted", img_right_undistorted)

                show_sr_images(valid_frame_found, left_img_sr, right_img_sr)

                print("\nFound valid frame for SR! Please review the windows and press: ")
                print("\t(Y/N) to accept/reject the frame")
                print("\t(F) to move on to the next step, choosing from selected frames")
                print("\t(Q) quit the program (STOPS THE PROGRAM, CAUTION!!!)")
                print("Frame currently shown: " + str(frame_num))
                print("Frames marked valid:   " + str(frames))
                key = cv2.waitKey(0)
                cv2.destroyAllWindows()
                cv2.waitKey(1)

                if key == get_keycode_from_key_code_entry(N_KEY):
                    print("Frame " + str(frame_num) + " rejected.")
                    break
                elif key == get_keycode_from_key_code_entry(Y_KEY):
                    frames.append(frame_num)
                    print("Frame " + str(frame_num) + " accepted.")
                    break
                elif key == get_keycode_from_key_code_entry(F_KEY):
                    print("\nMoving on to step 2!")
                    return frames
                elif key == get_keycode_from_key_code_entry(Q_KEY):
                    print("\nExiting now.")
                    sys.exit(0)
                else:
                    print("\nUnknown key pressed.")
            else:
                break

        frame_num = frame_num + 1


def display_no_frames_left_message(frames):
    """
    Helper function for the command line process step where no frames were selected for SR map generation.

    Prints out a bunch of messages saying that stereo rectification isn't possible and then stops the process.
    """
    print("\nNo frames selected for SR map generation.")
    print("If this was a mistake, add --first_frame " + str(frames[0]) + " to the script arguments and start from "
                                                                         "there.")
    print("Frame " + str(frames[0]) + " was the frame just rejected.")
    print("Exiting now.")
    sys.exit(0)


def select_final_frame_from_multiple_frames(frames, video_frame_loader, left_offset, right_offset):
    """Walks the user through the command line process step where the user has to select the final frame to use for SR
    map generation."""

    frame_tracker = FrameTracker(frames)

    while True:
        current_frame = frame_tracker.curr_frame()

        vc_obj_left_success, img_left = video_frame_loader.get_left_frame(current_frame + left_offset)
        vc_obj_right_success, img_right = video_frame_loader.get_right_frame(current_frame + right_offset)
        convert_to_gray(img_left)
        convert_to_gray(img_right)
        img_left_undistorted = undistort(img_left)
        img_right_undistorted = undistort(img_right)

        while True:
            valid_sr_frame, img_left_sr, img_right_sr = \
                generate_sr_map(img_left_undistorted, img_right_undistorted)
            show_sr_images(valid_sr_frame, img_left_sr, img_right_sr)

            print("\nFrame selection process has finished. Please review the windows and press:")
            print("(Left/Right Arrow Keys) to look through selected frames.")
            print("\t(N) remove currently displayed frame")
            print("\t(Z) undo the frame that last got removed")
            print("\t(R) restart from the beginning (Adds back in all the frames that got removed)")
            print("\t(S) select the frame to use for SR map generation.")
            print("\t(Q) quit the program (STOPS THE PROGRAM, CAUTION!!!)")
            print("Viewing the following frames: " + str(frames) + ". Current frame: " + str(current_frame))

            key = cv2.waitKey(0)
            cv2.destroyAllWindows()
            cv2.waitKey(1)

            if key == get_keycode_from_key_code_entry(LEFT_ARROW_KEY):
                frame_tracker.prev_frame()
                break
            elif key == get_keycode_from_key_code_entry(RIGHT_ARROW_KEY):
                frame_tracker.next_frame()
                break
            elif key == get_keycode_from_key_code_entry(N_KEY):
                frame_tracker.remove_current_frame()
                break
            elif key == get_keycode_from_key_code_entry(Z_KEY):
                frame_tracker.undo_remove_frame()
                break
            elif key == get_keycode_from_key_code_entry(R_KEY):
                frame_tracker.reset_frames()
                break
            elif key == get_keycode_from_key_code_entry(S_KEY):
                print("\nA file named \"" + SR_MAP_FILENAME + "\" has been generated with the SR map.\nFor "
                                                              "future use, this file is recommended to be "
                                                              "copied somewhere and renamed.")
                return current_frame
            elif key == get_keycode_from_key_code_entry(Q_KEY):
                print("Exiting now.")
                sys.exit(0)


def is_valid_sr_frame(left_img, right_img):
    """
    Returns True if the frame is valid for SR map generation and False if not

    :param left_img: Left image frame
    :param right_img: Right image frame
    :return: Whether or not the frame is valid for stereo rectification
    """

    img_left_corners_success, img_right_corners_success, _, _ = find_chessboard_corners(left_img, right_img)
    return img_left_corners_success and img_right_corners_success


def generate_sr_map(left_img, right_img):
    """
    Generates an SR map based only on the given frame.

    Try not to use this function. Stereo rectification should be based on as many frames as possible.
    """
    img_left_corners_success, img_right_corners_success, img_left_corner_coords, img_right_corner_coords = \
        find_chessboard_corners(left_img, right_img)

    if not (img_left_corners_success and img_right_corners_success):
        return False, None, None, None

    # Tuning these parameters does not appear to effect the end result
    max_iterations = 30
    epsilon = 0.0001
    criteria = (cv2.TERM_CRITERIA_MAX_ITER + cv2.TERM_CRITERIA_EPS, max_iterations, epsilon)

    # Create (x,y,z) object points for all intersections on checkerboard grid
    objp = np.zeros((CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)

    # Create empty arrays for object points and image points from each image
    objpoints = []
    img_points_left = []
    img_points_right = []

    # If found, add object points to objpoints array, and add image points (after refining them) to imgpoints array
    if img_left_corners_success and img_right_corners_success:
        objpoints.append(objp)

        # cornerSubPix refines the corner coordinates. (tuning these params does nothing)
        img_points_left = [cv2.cornerSubPix(left_img, img_left_corner_coords, (11, 11), (-1, -1), criteria)]
        img_points_right = [cv2.cornerSubPix(right_img, img_right_corner_coords, (11, 11), (-1, -1), criteria)]

        cv2.drawChessboardCorners(left_img, CHECKERBOARD, img_left_corner_coords, img_left_corners_success)
        cv2.drawChessboardCorners(right_img, CHECKERBOARD, img_right_corner_coords, img_right_corners_success)

    reprojection_error_left, cam_mtx_l, dist_l, rotation_vec_left, translation_vec_left = cv2.calibrateCamera(
        objpoints,
        img_points_left,
        left_img.shape[::-1],
        None, None)
    reprojection_error_right, cam_mtx_r, dist_r, rotation_vec_right, translation_vec_right = cv2.calibrateCamera(
        objpoints,
        img_points_right,
        right_img.shape[::-1],
        None, None)

    # getting optimal camera matrix and setting alpha to 0
    a = 0
    cam_mtx_l, _ = cv2.getOptimalNewCameraMatrix(cam_mtx_l, dist_l, left_img.shape[::-1], alpha=a)
    cam_mtx_r, _ = cv2.getOptimalNewCameraMatrix(cam_mtx_r, dist_r, right_img.shape[::-1], alpha=a)

    # https://docs.opencv.org/3.1.0/d9/d0c/group__calib3d.html#ga246253dcc6de2e0376c599e7d692303a
    img_left_corners_success, cam_mtx_l, dist_l, cam_mtx_r, dist_r, R, T, E, F = cv2.stereoCalibrate(
        objpoints,
        img_points_left,
        img_points_right,
        cam_mtx_l, dist_l, cam_mtx_r, dist_r,
        right_img.shape[::-1],
        flags=cv2.CALIB_SAME_FOCAL_LENGTH + cv2.CALIB_FIX_FOCAL_LENGTH + cv2.CALIB_ZERO_TANGENT_DIST)
    # cv2.CALIB_USE_INTRINSIC_GUESS

    # stereo rectify
    R1, R2, P1, P2, Q, validPixROI1, validPixROI2 = cv2.stereoRectify(cam_mtx_l,
                                                                      dist_l,
                                                                      cam_mtx_r,
                                                                      dist_r,
                                                                      right_img.shape[::-1],
                                                                      R, T, alpha=a)

    sr_map = SrMap(cam_mtx_l, dist_l, R1, P1, cam_mtx_r, dist_r, R2, P2)

    map_l, map_r = sr_map.generate_maps()

    new_img_left = cv2.remap(left_img,
                             map_l[0],
                             map_l[1],
                             cv2.INTER_LANCZOS4)
    new_img_right = cv2.remap(right_img,
                              map_r[0],
                              map_r[1],
                              cv2.INTER_LANCZOS4)

    for line in range(0, int(left_img.shape[0] / 20)):
        left_img[line * 20, :] = 255
        right_img[line * 20, :] = 255

    return True, new_img_left, new_img_right, sr_map


def find_chessboard_corners(left_img, right_img):
    """
    Finds and returns the chessboard corners based on the given images.

    :param left_img: Left image frame
    :param right_img: Right image frame
    :return: True and the corner coordinates if the chessboard was found, False if not
    """

    # For the 3rd argument, removing those parameters seems to have no effect
    img_left_corners_success, img_left_corner_coords = cv2.findChessboardCorners(left_img, CHECKERBOARD,
                                                                                 cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FILTER_QUADS)
    img_right_corners_success, img_right_corner_coords = cv2.findChessboardCorners(right_img, CHECKERBOARD,
                                                                                   cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FILTER_QUADS)
    return img_left_corners_success, img_right_corners_success, img_left_corner_coords, img_right_corner_coords


def show_sr_images(valid_sr_frame, img_left, img_right):
    """
    Shows the stereo rectified images.

    :param valid_sr_frame: If the given images are stereo rectified
    :param img_left: Stereo rectified left image frame
    :param img_right: Stereo rectified right iamge frame
    """
    if valid_sr_frame:
        left_window_title = "Left Image - Stereorectified"
        right_window_title = "Right Image - Stereorectified"
        cv2.imshow(left_window_title, img_left)
        cv2.imshow(right_window_title, img_right)
        cv2.moveWindow(left_window_title, 0, 0)
        cv2.moveWindow(right_window_title, img_left.shape[1], 0)
    else:
        print("The frame found is no longer valid for SR, this shouldn't happen.")


def undistort(img):
    """
    Undistorted the given OpenCV image.

    :param img: OpenCV image to be undistorted
    :return: Undistorted OpenCV image
    """
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    return undistorted_img


class FrameTracker:
    """Tracks selected and removed stereo rectified frames for the command line process step where the user is
    finding the best SR map to use from a list of stereo rectified frames."""

    def __init__(self, frames):
        """Constructor"""

        self.frames = frames
        self.removed_frames = []
        self.current_index = 0

    def next_frame(self):
        """Go to the next frame in the list if possible"""

        self.current_index = self.current_index + 1
        if self.current_index >= len(self.frames):
            self.current_index = len(self.frames) - 1
        return self.frames[self.current_index]

    def prev_frame(self):
        """Go to the previous frame in the list if possible"""

        self.current_index = self.current_index - 1
        if self.current_index < 0:
            self.current_index = 0
        return self.frames[self.current_index]

    def remove_current_frame(self):
        """Remove the current frame from the list"""

        if len(self.frames) == 1:
            display_no_frames_left_message(self.frames)

        removed_frame = self.frames.pop(self.current_index)
        self.removed_frames.append(removed_frame)

        if self.current_index >= len(self.frames):
            self.current_index = len(self.frames) - 1
            return self.frames[self.current_index]
        else:
            return self.frames[self.current_index]

    def undo_remove_frame(self):
        """Undo the last frame removed from the list"""

        if len(self.removed_frames) == 0:
            print("No frames have been removed.")
            return self.frames[self.current_index]

        current_frame = self.frames[self.current_index]
        self.frames.append(self.removed_frames.pop())
        self.frames.sort()
        self.current_index = self.frames.index(current_frame)
        return self.frames[self.current_index]

    def reset_frames(self):
        """Add back all the frames that were removed from the list before"""

        current_frame = self.frames[self.current_index]
        while len(self.removed_frames) > 0:
            self.frames.append(self.removed_frames.pop())
        self.frames.sort()
        self.current_index = self.frames.index(current_frame)
        return self.frames[self.current_index]

    def curr_frame(self):
        """Returns the current frame the user is viewing"""

        return self.frames[self.current_index]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("left_video", help="filename of the left video feed")
    parser.add_argument("right_video", help="filename of the right video feed")

    parser.add_argument("-o", "--show_original_frame", type=bool, default=False,
                        help="show original frame before undistortion and stereo rectification")
    parser.add_argument("-d", "--show_undistorted_frame", type=bool, default=False,
                        help="show frame after undistortion")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-l", "--left_offset", type=int, default=0,
                       help="offset of left video feed. left feed will start the specified amount of frames"
                            " earlier than normal")
    group.add_argument("-r", "--right_offset", type=int, default=0,
                       help="offset of right video feed. right feed will start the "
                            "specified amount of frames earlier than normal")
    parser.add_argument("-f", "--first_frame", type=int, default=0,
                        help="frame to start the videos on")
    args = parser.parse_args()

    if args.first_frame < 0:
        sys.exit("First frame must be greater than or equal to 0.")
    if args.left_offset < 0:
        sys.exit("Left offset must be greater than or equal to 0.")
    if args.right_offset < 0:
        sys.exit("Right offset must be greater than or equal to 0.")

    left_video_filename = args.left_video
    right_video_filename = args.right_video

    check_if_file_exists(left_video_filename)
    check_if_file_exists(right_video_filename)

    load_keycodes()
    find_and_generate_best_sr_map(left_video_filename, right_video_filename,
                                  left_offset=args.left_offset, right_offset=args.right_offset,
                                  first_frame=args.first_frame, show_original_frame=args.show_original_frame,
                                  show_undistorted_frame=args.show_undistorted_frame)
