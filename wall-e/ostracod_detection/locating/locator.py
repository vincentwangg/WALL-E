import numpy as np
import cv2
import sys
from ostracod import Ostracod



def calculate_location(image, mask):
    print "calculating loc"
    # calculate (x,y) location of the contour
    # this means abstracting the contour to a single point
    # by finding the centroid or something
    _, _, _, max_loc = cv2.minMaxLoc(image, mask=mask)
    return max_loc

def calculate_area(contour):
    # calculate area of a single contour
    print "calculating area"
    return cv2.contourArea(contour)

def calculate_brightness(image, mask):
    # calculate the brightness of a single contour
    print "calculating brightness"
    brightness = cv2.mean(image, mask=mask)
    return brightness[0]

def find_contours(threshold):
    # returns a list of contours in the image
    _, contours, _ = cv2.findContours(threshold, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    print "finding contours"
    return contours

def filter_image(image, threshold):
    # filter image
    # return filtered image
    retval, thresh = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
    print "filtering image"
    return thresh

def get_ostracods(filename):
    # filter image
    # find contours
    # compute area of each contour
    # compute brightness of each contour
    # compute x, y location of each contour
    # return list of ostracods
    print "get ostracods: "
    image = cv2.imread(filename)
    if image is None:
        sys.exit("unable to load image")
    imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    threshold = filter_image(imgray, 120)
    contours = find_contours(threshold)
    ostracod_list = []
    for c in contours:
        mask = np.zeros(imgray.shape, np.uint8)
        cv2.drawContours(mask, [c], 0, 255, -1)
        cv2.imshow("mask", mask)
        cv2.waitKey(0)
        brightness = calculate_brightness(imgray, mask)
        area = calculate_area(c)
        location = calculate_location(imgray, mask)
        if area >= 5:
            ostracod = Ostracod(location, area, brightness)
            ostracod_list.append(ostracod)

    for o in ostracod_list:
        print o.brightness, o.area, o.location
    return ostracod_list


def main():
    get_ostracods('../ostracod.png')


if __name__ == '__main__':
    main()
