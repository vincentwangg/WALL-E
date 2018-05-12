import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(ROOT_DIR, "config.txt")

ASSETS_PATH = os.path.join(os.path.dirname(ROOT_DIR), "assets")
IMG_NOT_AVAILABLE_FILENAME = "img_not_available.jpg"
WALLE_ICON = "walle_icon.png"

def get_asset_filename(file_basename):
    return os.path.join(ASSETS_PATH, file_basename)