# This script helps the user set up their keyboard so that OpenCV can read the button presses
# correctly.
#
# To use this in another script, call load_keycodes() from this script before any inputs from cv2.waitKey() are
# needed to process.
#
# To get a keycode, call get_keycode_from_key_code_entry() with the corresponding KeyCodeEntry object as the parameter.
#   For example, to get the keycode for the down arrow key, call load_keycodes(),
#     then call get_keycode_from_key_code_entry(DOWN_ARROW_KEY)

import ast
import cv2
import sys
import os.path
from definitions import CONFIG_PATH
import numpy as np


class KeyCodeEntry:
    def __init__(self, dict_name, message_text):
        self.dict_name = dict_name
        self.message_text = message_text
        self.keycode = -1

    def set_key_code(self, keycode):
        self.keycode = keycode


LEFT_ARROW_KEY = KeyCodeEntry("LEFT_ARROW_KEY", "left arrow key")
RIGHT_ARROW_KEY = KeyCodeEntry("RIGHT_ARROW_KEY", "right arrow key")
UP_ARROW_KEY = KeyCodeEntry("UP_ARROW_KEY", "up arrow key")
DOWN_ARROW_KEY = KeyCodeEntry("DOWN_ARROW_KEY", "down arrow key")
F_KEY = KeyCodeEntry("F_KEY", "\"F\" key")
N_KEY = KeyCodeEntry("N_KEY", "\"N\" key")
Q_KEY = KeyCodeEntry("Q_KEY", "\"Q\" key")
R_KEY = KeyCodeEntry("R_KEY", "\"R\" key")
S_KEY = KeyCodeEntry("S_KEY", "\"S\" key")
Y_KEY = KeyCodeEntry("Y_KEY", "\"Y\" key")
Z_KEY = KeyCodeEntry("Z_KEY", "\"Z\" key")
SPACE_KEY = KeyCodeEntry("SPACE_KEY", "space bar")

keycode_entries = [
    LEFT_ARROW_KEY, RIGHT_ARROW_KEY, UP_ARROW_KEY, DOWN_ARROW_KEY,
    F_KEY, N_KEY, Q_KEY, R_KEY, S_KEY, Y_KEY, Z_KEY,
    SPACE_KEY
]
keyname_to_KeyCodeEntry = {}
for entry in keycode_entries:
    keyname_to_KeyCodeEntry[entry.dict_name] = entry

keycodes = {}

blank_image = np.zeros((480, 640, 3), np.uint8)


def setup():
    print("Welcome to your first time key setup. This setup will only be run once for every new machine you use.")
    print()
    print("A blank window will appear. Please click on the window to bring it into \nfocus while keeping the console "
          "open to see further instructions.")
    print()
    print("WARNING: Make sure your CAPS lock is off!!")
    print("Mixing lowercase and uppercase letters will give\ndifferent key codes and might confuse you later on.")

    for entry in keycode_entries:
        print()
        print("Please press your " + entry.message_text + ".")
        keycode = show_blank_image()
        entry.keycode = keycode
        print("Recorded!")

    print()
    print("Your key codes have been registered. In order to verify that all your key codes are correct, please follow")
    print("the following instructions:")

    for entry in keycode_entries:
        print()
        print("Please press your " + entry.message_text + ".")
        keycode = show_blank_image()
        if keycode == entry.keycode:
            print("Verified!")
        else:
            print("The key you entered doesn't match the keycode recorded. The program will now stop.")
            print()
            print("Please run the following command:")
            print("python " + __file__)
            sys.exit()

    print()
    print("Writing to config.txt...")
    with open(CONFIG_PATH, 'w') as cfg_file:
        dict_string = "{"
        for entry in keycode_entries:
            dict_string = dict_string + "\"" + entry.dict_name + "\":" + str(entry.keycode) + ","
        dict_string = dict_string[:-1]
        dict_string = dict_string + "}"

        cfg_file.write(dict_string)
    print("Finished.")
    print()
    print("The setup is over. If this setup needs to be run again, run this command:")
    print("python " + __file__)


def show_blank_image():
    cv2.imshow("Blank window", blank_image)
    return cv2.waitKey(0)


def load_keycodes():
    if not os.path.isfile(CONFIG_PATH):
        setup()
    with open(CONFIG_PATH) as cfg_file:
        cfg_dictionary = ast.literal_eval(cfg_file.readline())
        for key in cfg_dictionary:
            keyname_to_KeyCodeEntry[key].keycode = cfg_dictionary[key]

    for entry in keycode_entries:
        keycodes[entry.dict_name] = entry.keycode


def get_keycode_from_key_code_entry(key_code_entry):
    return key_code_entry.keycode


if __name__ == '__main__':
    setup()
