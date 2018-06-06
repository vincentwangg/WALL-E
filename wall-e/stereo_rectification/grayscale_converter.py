"""
Contains functions for converting an OpenCV images to grayscale.
"""

import cv2


def convert_to_gray(img):
    """
    Converts an OpenCV image to grayscale.

    :param img: OpenCV image to convert to grayscale
    :return: a grayscale OpenCV image
    """

    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
