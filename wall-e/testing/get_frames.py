import sys
import cv2

board_size = (8,6)
frame_offset = 10

def find_corners(image, board_size):
    return cv2.findChessboardCorners(image, board_size, cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FILTER_QUADS)

def get_image_pair(possible_sizes, left_vc_obj, right_vc_obj):
    frames = []
    for size in possible_sizes:
        h, w = size
        print size
        count = 300
        left_vc_obj.set(cv2.CAP_PROP_POS_FRAMES, count)  # 3821
        success, left_image = left_vc_obj.read()
        while success:
            if count == 1200: break
            count = count + 1
            img_left_corners_success, img_left_corner_coords = find_corners(left_image, size)
            if img_left_corners_success:
                right_vc_obj.set(cv2.CAP_PROP_POS_FRAMES, count + frame_offset)
                succ, right_image = right_vc_obj.read()
                cv2.flip(right_image, -1, right_image)
                img_right_corners_success, img_right_corner_coords = find_corners(right_image, size)
                if img_right_corners_success:
                    print "found matching pair: ", h, w, "at count: ", count
                    frames.append(count)
            success, left_image = left_vc_obj.read()
    print frames
    if not frames:
        sys.exit("NO IMAGE PAIRS FOUND!")


def main():
    left = cv2.VideoCapture("../Left.mkv")
    right = cv2.VideoCapture("../Right.mkv")
    get_image_pair([board_size],left,right)


if __name__ == '__main__':
    main()