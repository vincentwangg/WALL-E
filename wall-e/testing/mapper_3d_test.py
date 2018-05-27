from ostracod_detection.matching.match import match
from cv2 import imread
from mapping_3d.mapper_3d import depth_map
from mapping_3d.pulse_data import FramePulseData
from mapping_3d.camera import Camera


def main():
    framenum = 40890
    left_filename = "../../images/" + str(framenum) + "_ostracod_left.jpg"
    right_filename = "../../images/" + str(framenum) + "_ostracod_right.jpg"
    left = imread(left_filename)
    right = imread(right_filename)
    fpd = FramePulseData()

    ostracod_list_l, ostracod_list_r = match(left, right)
    camera = Camera(baseline=500, focal_length=5)
    depth_map(ostracod_list_l, ostracod_list_r, framepulsedata=fpd, framenum=0, camera=camera)
    print fpd



if __name__ == '__main__':
    main()