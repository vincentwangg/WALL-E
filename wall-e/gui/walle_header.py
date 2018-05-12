import cv2
from tkinter import *
from definitions import *
from gui.gui_base_frame import GuiBaseFrame
from utilities.image_converter import cv2_image_to_tkinter_with_resize

WALLE_ICON_WIDTH = 292
WALLE_ICON_HEIGHT = 103

class WalleHeader(GuiBaseFrame):
    def __init__(self, parent, controller):
        GuiBaseFrame.__init__(self, parent, controller)

    def setup_widgets(self):
        walle_icon = cv2.imread(get_asset_filename(WALLE_ICON))
        walle_icon = cv2_image_to_tkinter_with_resize(walle_icon, WALLE_ICON_WIDTH, WALLE_ICON_HEIGHT)

        self.walle_icon_label = Label(self, image=walle_icon)
        self.walle_icon_label.image = walle_icon

        self.walle_icon_label.grid(row=0, column=0, columnspan=2)

