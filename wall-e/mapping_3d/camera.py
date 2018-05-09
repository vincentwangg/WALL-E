import cv2
import sys
from stereo_rectification.apply_sr import undistort
from stereo_rectification.apply_sr import generate_maps
from stereo_rectification.apply_sr import apply_rectify_maps

class Camera:
    def __init__(self, baseline, focal_length=None):
        if focal_length is None:
            self.focal_length = self.get_focal_length()
        else:
            self.focal_length = focal_length
        self.baseline = baseline


    def get_focal_length(self): # needs video and access to sr_map
        checkerboard_distance = 5 # how far away the checkerboard is from the camera
        width_of_one_square = 2
        optimal_frame_num = 10
        calibration_video = cv2.VideoCapture("../../videos/45_r_check.mkv")
        sr_yml_filename = "../stereo_rectification/sr_map.yml"

        (l_map, r_map) = generate_maps(sr_yml_filename)

        if optimal_frame_num > 0:
            calibration_video.set(cv2.CAP_PROP_POS_FRAMES, optimal_frame_num-1)

        success, image = calibration_video.read()

        if not success:
            sys.exit("image failed to load!")

        image = undistort(image)
        image = apply_rectify_maps(image, r_map[0], r_map[1])
        # cv2.imshow("undistorted_sr", image)
        # cv2.waitKey(0)
        success, img_coords = cv2.findChessboardCorners(image, (4, 3),
                                                        cv2.CALIB_CB_ADAPTIVE_THRESH +
                                                        cv2.CALIB_CB_FILTER_QUADS)
        if not success:
            sys.exit("failed to find checkerboard corners in image")

        image_2 = cv2.drawChessboardCorners(image, (4, 4), img_coords, success)
        # cv2.imshow("checkerboard", image_2)
        # cv2.waitKey(0)
        max_iterations = 30
        epsilon = 0.0001
        criteria = (cv2.TERM_CRITERIA_MAX_ITER + cv2.TERM_CRITERIA_EPS, max_iterations, epsilon)
        imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        img_points = [cv2.cornerSubPix(imgray, img_coords, (11, 11), (-1, -1), criteria)]

        pixel_distance = img_points[0][0][0][0] - img_points[0][1][0][0]

        focal_length = checkerboard_distance*pixel_distance/width_of_one_square

        return focal_length

def main():
    camera = Camera(baseline=500)
    print "baseline:", camera.baseline, "focal length: ", camera.focal_length

if __name__ == '__main__':
    main()
