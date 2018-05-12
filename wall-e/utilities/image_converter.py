import cv2
from PIL import Image, ImageTk


def cv2_image_to_tkinter_with_resize(img, width, height):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    img = img.resize((width, height), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    return img


def cv2_image_to_tkinter(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)
    img = ImageTk.PhotoImage(img)
    return img
