import numpy as np
import cv2
import sys

# You should replace these 3 lines with the output in calibration step
DIM=(478, 276)
K=np.array([[158.90756071525877, 0.0, 237.55632881503345], [0.0, 159.10443431704135, 133.46049020836293], [0.0, 0.0, 1.0]])
D=np.array([[-0.15062519034668467], [-0.005567590452705028], [0.05244142023188127], [-0.027974989825770607]])
def undistort(img_path):
    img = cv2.imread(img_path)
    h,w = img.shape[:2]
    map1, map2 = cv2.fisheye.initUndistortRectifyMap(K, D, np.eye(3), K, DIM, cv2.CV_16SC2)
    undistorted_img = cv2.remap(img, map1, map2, interpolation=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
    cv2.imshow("undistorted", undistorted_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
if __name__ == '__main__':
    for p in sys.argv[1:]:
        undistort(p)