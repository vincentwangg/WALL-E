# Code imported from https://medium.com/@kennethjiang/calibrate-fisheye-lens-using-opencv-part-2-13990f1b157f

import argparse
from config.keycode_setup import *
from stereo_rectification.grayscale_converter import convert_to_gray
from utilities.video_frame_loader import VideoFrameLoader
from utilities.yaml_utility import save_to_yml

# You should replace these 3 lines with the output in calibration step (calibrate.py)
CHECKERBOARD = (8, 6)
DIM = (640, 478)  # deinterlaced video is now 640 X 478
K = np.array(
    [[526.756924435422, 0.0, 330.221556181272], [0.0, 478.43311043812145, 249.44524334088075], [0.0, 0.0, 1.0]])
D = np.array([[-0.07527166402108293], [0.006777363197177597], [-0.32231954249568173], [0.43735394851622683]])

map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_32F)

SR_MAP_GENERATED_FILENAME = "sr_map.yml"
SR_MAP_GENERATED_MESSAGE = "\nA file named \"" + SR_MAP_GENERATED_FILENAME + "\" has been generated with the SR " \
                                                                             "map!\nFor future use, this file is " \
                                                                             "recommended to be copied somewhere and " \
                                                                             "renamed. "


def find_and_generate_best_sr_map(left_video_filename, right_video_filename,
                                  left_offset=0, right_offset=0,
                                  first_frame=0, show_original_frame=False, show_undistorted_frame=False):
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
            generate_and_save_sr_maps(img_left_undistorted, img_right_undistorted)

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

        generate_and_save_sr_maps(img_left_undistorted, img_right_undistorted)


def find_valid_frames_for_sr(frame_num, left_offset, right_offset, show_original_frame, show_undistorted_frame,
                             video_frame_loader):
    frames = []

    while True:
        vc_obj_left_success, img_left = video_frame_loader.get_left_frame(frame_num + left_offset)
        vc_obj_right_success, img_right = video_frame_loader.get_right_frame(frame_num + right_offset)

        if not vc_obj_left_success or not vc_obj_right_success:
            print("Reached the end of video")
            break

        img_left_undistorted = convert_to_gray(undistort(img_left))
        img_right_undistorted = convert_to_gray(undistort(img_right))

        while True:
            generate_and_save_sr_maps(img_left_undistorted, img_right_undistorted)

            if show_original_frame:
                cv2.imshow("Original Left", img_left)
                cv2.imshow("Original Right", img_right)
            if show_undistorted_frame:
                cv2.imshow("Left Undistorted", img_left_undistorted)
                cv2.imshow("Right Undistorted", img_right_undistorted)

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

        frame_num = frame_num + 1

    return frames


def display_no_frames_left_message(frames):
    print("\nNo frames selected for SR map generation.")
    print("If this was a mistake, add --first_frame " + str(frames[0]) + " to the script arguments and start from "
                                                                         "there.")
    print("Frame " + str(frames[0]) + " was the frame just rejected.")
    print("Exiting now.")
    sys.exit(0)


def select_final_frame_from_multiple_frames(frames, video_frame_loader, left_offset, right_offset):
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
            generate_and_save_sr_maps(convert_to_gray(img_left_undistorted), convert_to_gray(img_right_undistorted))
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
                print("\nA file named \"" + SR_MAP_GENERATED_FILENAME + "\" has been generated with the SR map.\nFor "
                                                                        "future use, this file is recommended to be "
                                                                        "copied somewhere and renamed.")
                return current_frame
            elif key == get_keycode_from_key_code_entry(Q_KEY):
                print("Exiting now.")
                sys.exit(0)


def generate_and_save_sr_maps(img_left, img_right):
    # For the 3rd argument, removing those parameters seems to have no effect
    img_left_corners_success, img_left_corner_coords = cv2.findChessboardCorners(img_left, CHECKERBOARD,
                                                                                 cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FILTER_QUADS)
    img_right_corners_success, img_right_corner_coords = cv2.findChessboardCorners(img_right, CHECKERBOARD,
                                                                                   cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FILTER_QUADS)

    # print "Detected corners in left image:\t\t" + str(img_right_corners_success)
    # print "Detected corners in right image:\t" + str(img_left_corners_success)

    if not (img_left_corners_success and img_right_corners_success):
        return False

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
        img_points_left = [cv2.cornerSubPix(img_left, img_left_corner_coords, (11, 11), (-1, -1), criteria)]
        img_points_right = [cv2.cornerSubPix(img_right, img_right_corner_coords, (11, 11), (-1, -1), criteria)]

        cv2.drawChessboardCorners(img_left, CHECKERBOARD, img_left_corner_coords, img_left_corners_success)
        cv2.drawChessboardCorners(img_right, CHECKERBOARD, img_right_corner_coords, img_right_corners_success)

    reprojection_error_left, cam_mtx_l, dist_l, rotation_vec_left, translation_vec_left = cv2.calibrateCamera(
        objpoints,
        img_points_left,
        img_left.shape[::-1],
        None, None)
    reprojection_error_right, cam_mtx_r, dist_r, rotation_vec_right, translation_vec_right = cv2.calibrateCamera(
        objpoints,
        img_points_right,
        img_right.shape[::-1],
        None, None)

    # getting optimal camera matrix and setting alpha to 0
    a = 0
    cam_mtx_l, _ = cv2.getOptimalNewCameraMatrix(cam_mtx_l, dist_l, img_left.shape[::-1], alpha=a)
    cam_mtx_r, _ = cv2.getOptimalNewCameraMatrix(cam_mtx_r, dist_r, img_right.shape[::-1], alpha=a)

    # https://docs.opencv.org/3.1.0/d9/d0c/group__calib3d.html#ga246253dcc6de2e0376c599e7d692303a
    img_left_corners_success, cam_mtx_l, dist_l, cam_mtx_r, dist_r, R, T, E, F = cv2.stereoCalibrate(
        objpoints,
        img_points_left,
        img_points_right,
        cam_mtx_l, dist_l, cam_mtx_r, dist_r,
        img_right.shape[::-1],
        flags=cv2.CALIB_SAME_FOCAL_LENGTH + cv2.CALIB_FIX_FOCAL_LENGTH + cv2.CALIB_ZERO_TANGENT_DIST)
    # cv2.CALIB_USE_INTRINSIC_GUESS

    # stereo rectify
    R1, R2, P1, P2, Q, validPixROI1, validPixROI2 = cv2.stereoRectify(cam_mtx_l,
                                                                      dist_l,
                                                                      cam_mtx_r,
                                                                      dist_r,
                                                                      img_right.shape[::-1],
                                                                      R, T, alpha=a)

    map_l = cv2.initUndistortRectifyMap(cam_mtx_l,
                                        dist_l,
                                        R1, P1,
                                        img_left.shape[::-1],
                                        cv2.CV_32F)
    map_r = cv2.initUndistortRectifyMap(cam_mtx_r,
                                        dist_r,
                                        R2, P2,
                                        img_right.shape[::-1],
                                        cv2.CV_32F)

    save_to_yml(SR_MAP_GENERATED_FILENAME, "cam_mtx_l", cam_mtx_l, w=1)
    save_to_yml(SR_MAP_GENERATED_FILENAME, "dist_l", dist_l)
    save_to_yml(SR_MAP_GENERATED_FILENAME, "R1", R1)
    save_to_yml(SR_MAP_GENERATED_FILENAME, "P1", P1)

    save_to_yml(SR_MAP_GENERATED_FILENAME, "cam_mtx_r", cam_mtx_r)
    save_to_yml(SR_MAP_GENERATED_FILENAME, "dist_r", dist_r)
    save_to_yml(SR_MAP_GENERATED_FILENAME, "R2", R2)
    save_to_yml(SR_MAP_GENERATED_FILENAME, "P2", P2)

    img_left = cv2.remap(img_left,
                         map_l[0],
                         map_l[1],
                         cv2.INTER_LANCZOS4)
    img_right = cv2.remap(img_right,
                          map_r[0],
                          map_r[1],
                          cv2.INTER_LANCZOS4)

    for line in range(0, int(img_left.shape[0] / 20)):
        img_left[line * 20, :] = 255
        img_right[line * 20, :] = 255

    left_window_title = "Left Image - Stereorectified"
    right_window_title = "Right Image - Stereorectified"

    cv2.imshow(left_window_title, img_left)
    cv2.imshow(right_window_title, img_right)

    cv2.moveWindow(left_window_title, 0, 0)
    cv2.moveWindow(right_window_title, img_left.shape[1], 0)

    return True


def undistort(img):
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    return undistorted_img


class FrameTracker:
    def __init__(self, frames):
        self.frames = frames
        self.removed_frames = []
        self.current_index = 0

    def next_frame(self):
        self.current_index = self.current_index + 1
        if self.current_index >= len(self.frames):
            self.current_index = len(self.frames) - 1
        return self.frames[self.current_index]

    def prev_frame(self):
        self.current_index = self.current_index - 1
        if self.current_index < 0:
            self.current_index = 0
        return self.frames[self.current_index]

    def remove_current_frame(self):
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
        if len(self.removed_frames) == 0:
            print("No frames have been removed.")
            return self.frames[self.current_index]

        current_frame = self.frames[self.current_index]
        self.frames.append(self.removed_frames.pop())
        self.frames.sort()
        self.current_index = self.frames.index(current_frame)
        return self.frames[self.current_index]

    def reset_frames(self):
        current_frame = self.frames[self.current_index]
        while len(self.removed_frames) > 0:
            self.frames.append(self.removed_frames.pop())
        self.frames.sort()
        self.current_index = self.frames.index(current_frame)
        return self.frames[self.current_index]

    def curr_frame(self):
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

    load_keycodes()
    find_and_generate_best_sr_map(args.left_video, args.right_video,
                                  left_offset=args.left_offset, right_offset=args.right_offset,
                                  first_frame=args.first_frame, show_original_frame=args.show_original_frame,
                                  show_undistorted_frame=args.show_undistorted_frame)
