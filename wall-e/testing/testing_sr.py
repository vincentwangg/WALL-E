import cv2
import stereorectification


def get_images(frame_num, offset, left, right):
    left.set(cv2.CAP_PROP_POS_FRAMES,frame_num)
    right.set(cv2.CAP_PROP_POS_FRAMES,frame_num + offset)
    suc, l_image = left.read()
    suc, r_image = right.read()
    return l_image, r_image


def show(left, right):
    cv2.imshow("left", left)
    cv2.imshow("right", right)
    cv2.waitKey(0)

def get_f(video):
    video.set(cv2.CAP_PROP_POS_FRAMES,2700)
    succ, image = video.read()
    image[260,306] = 255
    cv2.imshow("og_image",image)
    cv2.waitKey(0)

def main():
    frame_num = 1650
    offset = 13
    org_left = cv2.VideoCapture('../Flat_rightview.mkv')
    left = cv2.VideoCapture('../Flat_leftview_stereo_rectified.mkv')
    right = cv2.VideoCapture('../Flat_rightview_stereo_rectified.mkv')
    left_image, right_image = get_images(frame_num, offset, left, right)
    for line in range(0, int(left_image.shape[0] / 20)):
        left_image[line * 20, :] = 0,0,255
        right_image[line * 20, :] = 0,0,255
    # cv2.cvtColor(left_image,left_image, cv2.COLOR_GRAY2RGB)
    # cv2.cvtColor(right_image, right_image, cv2.COLOR_GRAY2RGB)

    right_image[260, 314] = 255
    left_image[260, 381] = 255
    show(left_image, right_image)
    # get_f(org_left)
    # left image is 351
    # right image is 314



if __name__ == '__main__':
    main()