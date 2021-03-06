import os

TMP_FOLDER_NAME = "tmp"
STEREO_RECTIFICATION_DIR_NAME = "stereo_rectification"
MAPPING_3D_DIR_NAME = "mapping_3d"

# Root directory is ~/WALL-E/wall-e (Where all the source code is)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Project directory is ~/WALL-E (Where all the project files are)
PROJECT_DIR = os.path.abspath(os.path.join(ROOT_DIR, os.pardir))

TMP_FOLDER_PATH = os.path.abspath(os.path.join(PROJECT_DIR, TMP_FOLDER_NAME))
CONFIG_PATH = os.path.join(ROOT_DIR, ".keybindings.cfg")
GUI_CACHE_PATH = os.path.join(ROOT_DIR, ".gui_cache.txt")

STEREO_RECTIFICATION_DIR = os.path.join(ROOT_DIR, STEREO_RECTIFICATION_DIR_NAME)
MAPPING_3D_DIR = os.path.join(ROOT_DIR, MAPPING_3D_DIR_NAME)

ASSETS_PATH = os.path.join(os.path.dirname(ROOT_DIR), "assets")
IMG_NOT_AVAILABLE_FILENAME = "img_not_available.jpg"
WALLE_ICON = "walle_icon.png"

def get_asset_filename(file_basename):
    return os.path.join(ASSETS_PATH, file_basename)