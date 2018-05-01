import numpy as np
import cv2
import sys
from ostracod import Ostracod



def calculate_location(image, mask):
    # calculate (x,y) location of the contour
    # this means abstracting the contour to a single point
    # by finding the centroid or something
    _, _, _, max_loc = cv2.minMaxLoc(image, mask=mask)
    return max_loc

def calculate_area(contour):
    # calculate area of a single contour
    return cv2.contourArea(contour)

def calculate_brightness(image, mask):
    # calculate the brightness of a single contour
    brightness = cv2.mean(image, mask=mask)
    return brightness[0]

def find_contours(threshold):
    # returns a list of contours in the image
    # in the future we may want to vet to eliminate the edge case where multiple ostracods count as 1 contour
    _, contours, _ = cv2.findContours(threshold, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def filter_image(image, threshold):
    # filter image
    # return filtered image
    retval, thresh = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
    return thresh

def get_ostracods(image):
    # filter image
    # find contours
    # compute area of each contour
    # compute brightness of each contour
    # compute x, y location of each contour
    # return list of ostracods
    print "Ostracods: "
    if image is None:
        sys.exit("unable to load image")
    imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    threshold = filter_image(imgray, 120)
    contours = find_contours(threshold)
    ostracod_list = []
    x_cor = []
    for c in contours:
        mask = np.zeros(imgray.shape, np.uint8)
        cv2.drawContours(mask, [c], 0, 255, -1)
        brightness = calculate_brightness(imgray, mask)
        area = calculate_area(c)
        location = calculate_location(imgray, mask)
        if area >= 5:
            x_cor.append(location[0])
            ostracod = Ostracod(location, area, brightness)
            ostracod_list.append(ostracod)

    mean_x_cor = np.mean(x_cor)
    for o in ostracod_list:
        o.distance_from_mean = o.location[0] - mean_x_cor

    print "Brightness", "\tArea", "\tLocation", "\tdistance_from_mean"
    for o in ostracod_list:
        print round(o.brightness, 2), "\t\t", o.area, "\t", o.location, "\t", o.distance_from_mean
    return ostracod_list


def main():
    image = cv2.imread('../../../images/ostracod.png')
    get_ostracods(image)


if __name__ == '__main__':
    main()
