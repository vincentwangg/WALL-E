# Code imported from https://medium.com/@kennethjiang/calibrate-fisheye-lens-using-opencv-part-2-13990f1b157f

import numpy as np
import cv2
import sys

# You should replace these 3 lines with the output in calibration step
DIM=(640, 480)
K=np.array([[505.3019653100971, 0.0, 367.1536189100808], [0.0, 463.0239595310009, 262.27198974329553], [0.0, 0.0, 1.0]])
D=np.array([[-0.10747340220009194], [-0.23322478481242945], [0.956438056950602], [-1.647891946278236]])

def undistort(img_path):
    vc_obj_right = cv2.VideoCapture("../Right.ASF")
    vc_obj_right.set(cv2.CAP_PROP_POS_FRAMES, 740)
    vc_obj_right_success, img = vc_obj_right.read()
    cv2.imshow("original", img)
    h, w = img.shape[:2]
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    cv2.imshow("undistorted", undistorted_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    for p in sys.argv[1:]:
        undistort(p)