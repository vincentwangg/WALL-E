import ostracod_detection.matching.match as match
from stereo_rectification.sr_map_gen import undistort
from ostracod_detection.locating import locator
import random
import cv2



def component():
  return random.randint(0, 255)

def random_color():
    return component(), component(), component()


def draw_circle(image, coordinates, color):
    loc = (coordinates[0], coordinates[1])
    cv2.circle(image, loc, 8, color, thickness=3, lineType=8, shift=0)



def main():
    framenum = 40890
    left_filename = "../../images/" + str(framenum) + "_ostracod_left.jpg"
    right_filename = "../../images/" + str(framenum) + "_ostracod_right.jpg"
    image_l = cv2.imread(left_filename)
    image_l = undistort(image_l)
    image_r = cv2.imread(right_filename)
    image_r = undistort(image_r)

    ostracod_list_l = locator.get_ostracods(image_l)
    ostracod_list_r = locator.get_ostracods(image_r)

    l_list, r_list = match.match(ostracod_list_l, ostracod_list_r, threshold=5)
    for o in l_list:
        if len(o.matches) > 0:
            color = random_color()
            draw_circle(image_l, o.location, color)
            for m in o.matches:
                draw_circle(image_r, r_list[m[0]].location, color)
    cv2.imshow("left matched", image_l)
    cv2.imshow("right_matched", image_r)
    cv2.waitKey(0)


if __name__ == '__main__':
    main()
