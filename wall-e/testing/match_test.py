from ostracod_detection.matching.match import match
import random
import cv2



def component():
  return random.randint(0, 255)

def random_color():
    return component(), component(), component()


def draw_circle(image, coordinates, color):
    cv2.circle(image, coordinates, 8, color, thickness=1, lineType=8, shift=0)



def main():
    framenum = 40890
    left_filename = "../../images/" + str(framenum) + "_ostracod_left.jpg"
    right_filename = "../../images/" + str(framenum) + "_ostracod_right.jpg"
    image_l = cv2.imread(left_filename)
    image_r = cv2.imread(right_filename)
    l_list, r_list = match(left_filename, right_filename)
    for o in l_list:
        if len(o.matches) > 0:
            color = random_color()
            draw_circle(image_l, o.location, color)
            for m in o.matches:
                draw_circle(image_r, r_list[m].location, color)
    cv2.imshow("left matched", image_l)
    cv2.imshow("right_matched", image_r)
    cv2.waitKey(0)


if __name__ == '__main__':
    main()