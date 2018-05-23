from stereo_rectification.apply_sr import undistort
from stereo_rectification.apply_sr import generate_maps
from stereo_rectification.apply_sr import apply_rectify_maps
from stereo_rectification.sr_map_gen import SR_MAP_GENERATED_FILENAME
from definitions import PROJECT_ROOT_PATH, SRC_PATH
from config.keycode_setup import *
from utilities.file_checker import check_if_file_exists

# TODO: Take a video of a checkerboard at a known distance

class Camera:
    def __init__(self, baseline, focal_length=None):
        if focal_length is None:
            self.focal_length = self.get_focal_length()
        else:
            self.focal_length = focal_length
        self.baseline = baseline


    def get_focal_length(self): # needs video and access to sr_map
        load_keycodes()
        checkerboard_shape = (3, 3)
        checkerboard_distance = 383 # how far away the checkerboard is from the camera in mm
        width_of_one_square = 26 # mm
        start_frame_num = 1
        vid_filename = PROJECT_ROOT_PATH + "/videos/focal_length_calib.mkv"

        check_if_file_exists(vid_filename)

        calibration_video = cv2.VideoCapture(vid_filename)
        sr_yml_filename = SRC_PATH + "/stereo_rectification/" + "wes_14246_csfl_cffl_cztd.yml"

        check_if_file_exists(sr_yml_filename)

        (l_map, r_map) = generate_maps(sr_yml_filename)
        if start_frame_num > 0:
            calibration_video.set(cv2.CAP_PROP_POS_FRAMES, start_frame_num-1)


        success, image = calibration_video.read()
        frame_num = start_frame_num
        found_check = False
        if not success:
            sys.exit("video failed to load in function get_focal_length() of camera.py!")

        while success:
            image = undistort(image)
            image = apply_rectify_maps(image, r_map[0], r_map[1])
            found_check, img_coords = cv2.findChessboardCorners(image, checkerboard_shape,
                                                            cv2.CALIB_CB_ADAPTIVE_THRESH +
                                                            cv2.CALIB_CB_FILTER_QUADS)

            if found_check:
                print "Frame num: ", frame_num
                image_2 = cv2.drawChessboardCorners(image.copy(), checkerboard_shape, img_coords, success)

                cv2.imshow("focal_length_calibration_checkerboard", image_2)
                print "Accept Frame? (Y/N)"
                print "Quit the program. CAUTION!! (Q)"
                key = cv2.waitKey(0)
                cv2.destroyAllWindows()
                if key == get_keycode_from_key_code_entry(Q_KEY):
                    sys.exit("Quiting program... GOODBYE")
                elif key == get_keycode_from_key_code_entry(Y_KEY):
                    break
                elif key == get_keycode_from_key_code_entry(N_KEY):
                    continue
            success, image = calibration_video.read()
            frame_num += 1

        if not found_check:
            sys.exit("could not find checkerboard in calibration video in function get_focal_length() of camera.py\n"
                     "Make sure that the correct sr_map is being read")

        max_iterations = 30
        epsilon = 0.0001
        criteria = (cv2.TERM_CRITERIA_MAX_ITER + cv2.TERM_CRITERIA_EPS, max_iterations, epsilon)
        imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        img_points = [cv2.cornerSubPix(imgray, img_coords, (11, 11), (-1, -1), criteria)]

        print "On to the next round!!!"
        x_1 = None
        x_2 = None
        while (x_1 is None or x_2 is None):
            for i in xrange(1, 9):
                loc1 = (int(img_points[0][0][0][0]), int(img_points[0][0][0][1]))
                loc2 = (int(img_points[0][i][0][0]), int(img_points[0][i][0][1]))

                copy = image_2.copy()

                cv2.circle(copy, loc1, 8, (255, 0, 0), thickness=3, lineType=8, shift=0)
                cv2.circle(copy, loc2, 8, (255, 0, 0), thickness=3, lineType=8, shift=0)

                cv2.imshow("image", copy)
                print ""
                print "Select points that are 1 square away in the x direction."
                print "Accept Frame? (Y/N)"
                print "Quit the program. CAUTION!! (Q)"
                key = cv2.waitKey(0)
                cv2.destroyAllWindows()

                if key == get_keycode_from_key_code_entry(Q_KEY):
                    sys.exit("Quiting program... GOODBYE")
                elif key == get_keycode_from_key_code_entry(Y_KEY):
                    x_1 = loc1[0]
                    x_2 = loc2[0]
                    break
                elif key == get_keycode_from_key_code_entry(N_KEY):
                    continue


        pixel_distance = abs(x_1 - x_2)

        focal_length = checkerboard_distance*pixel_distance/width_of_one_square
        print "focal length: ", focal_length
        return focal_length

def main():
    camera = Camera(baseline=500)
    print "baseline:", camera.baseline, "focal length: ", camera.focal_length

if __name__ == '__main__':
    main()
