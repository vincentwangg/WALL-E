import ast
from tkinter import *
from tkinter import filedialog

import cv2

from definitions import *
from gui.pipeline1.constants import VIDEO_PREVIEW_WIDTH, VIDEO_PREVIEW_HEIGHT, SCREENS_REL_X, VIDEO_SELECT_SCREEN_REL_Y, \
    VIDEOS_SELECTED_TMP_FILENAME, LEFT, RIGHT
from gui.widgets.gui_base_frame import GuiBaseFrame
from gui.widgets.header1_label import Header1Label
from gui.widgets.p_label import PLabel
from utilities.image_converter import cv2_bgr_image_to_tkinter_with_resize
from utilities.tmp_file_writer import write_to_tmp_file, read_tmp_file, does_tmp_file_exist_basename

SCREEN_TITLE_ROW = 0
INSTRUCTION_ROW = SCREEN_TITLE_ROW + 1
THUMBNAIL_ROW = INSTRUCTION_ROW + 1
FILENAME_PREVIEW_ROW = THUMBNAIL_ROW + 1
CHOOSE_VIDEO_BUTTON_ROW = FILENAME_PREVIEW_ROW + 1
NEXT_BUTTON_ROW = CHOOSE_VIDEO_BUTTON_ROW + 1

LEFT_VIDEO_THUMBNAIL_COL = 0
RIGHT_VIDEO_THUMBNAIL_COL = 1

CENTER_SCREEN_COLSPAN = 2


class VideoSelectionScreen(GuiBaseFrame):
    def __init__(self, parent, controller, **kw):
        GuiBaseFrame.__init__(self, parent, controller, **kw)

    def setup_widgets(self):
        self.content_wrapper = Frame(self)

        self.content_wrapper.grid_columnconfigure(0, weight=1)
        self.content_wrapper.grid_columnconfigure(1, weight=1)

        self.init_video_info()

        self.screen_title_label = Header1Label(self.content_wrapper, text="Video Selection")
        self.instruction_label = PLabel(self.content_wrapper, text="Please choose your left and right video files.")
        self.left_video_filename_preview_label = PLabel(self.content_wrapper, text="No Video Selected")
        self.left_video_button = Button(self.content_wrapper, text="Choose Left Video",
                                        command=lambda: self.select_video_through_button_press(LEFT))
        self.right_video_filename_preview_label = PLabel(self.content_wrapper, text="No Video Selected")
        self.right_video_button = Button(self.content_wrapper, text="Choose Right Video",
                                         command=lambda: self.select_video_through_button_press(RIGHT))
        self.next_button = Button(self.content_wrapper, text="Next", state=DISABLED,
                                  command=lambda: self.next_screen())

        self.add_img_previews()

        self.screen_title_label.grid(row=SCREEN_TITLE_ROW, column = 0, columnspan=CENTER_SCREEN_COLSPAN)
        self.instruction_label.grid(row=INSTRUCTION_ROW, column=LEFT_VIDEO_THUMBNAIL_COL,
                                    columnspan=CENTER_SCREEN_COLSPAN)

        self.left_video_thumbnail.grid(row=THUMBNAIL_ROW, column=LEFT_VIDEO_THUMBNAIL_COL)
        self.left_video_filename_preview_label.grid(row=FILENAME_PREVIEW_ROW, column=LEFT_VIDEO_THUMBNAIL_COL)
        self.left_video_button.grid(row=CHOOSE_VIDEO_BUTTON_ROW, column=LEFT_VIDEO_THUMBNAIL_COL)

        self.right_video_thumbnail.grid(row=THUMBNAIL_ROW, column=RIGHT_VIDEO_THUMBNAIL_COL)
        self.right_video_filename_preview_label.grid(row=FILENAME_PREVIEW_ROW, column=RIGHT_VIDEO_THUMBNAIL_COL)
        self.right_video_button.grid(row=CHOOSE_VIDEO_BUTTON_ROW, column=RIGHT_VIDEO_THUMBNAIL_COL)

        self.next_button.grid(row=NEXT_BUTTON_ROW, column=0, columnspan=CENTER_SCREEN_COLSPAN)
        self.content_wrapper.place(relx=SCREENS_REL_X, rely=VIDEO_SELECT_SCREEN_REL_Y, anchor=CENTER)

    def init_video_info(self):
        self.left_video_selected = False
        self.right_video_selected = False
        self.left_video_filename = None
        self.right_video_filename = None

    def next_screen(self):
        self.controller.set_video_filenames(self.left_video_filename, self.right_video_filename)
        self.controller.show_next_frame()

    def add_img_previews(self):
        img_not_available = cv2.imread(get_asset_filename(IMG_NOT_AVAILABLE_FILENAME))
        img_not_available = cv2_bgr_image_to_tkinter_with_resize(img_not_available, VIDEO_PREVIEW_WIDTH, VIDEO_PREVIEW_HEIGHT)

        self.left_video_thumbnail = Label(self.content_wrapper, image=img_not_available)
        self.left_video_thumbnail.image = img_not_available
        self.right_video_thumbnail = Label(self.content_wrapper, image=img_not_available)
        self.right_video_thumbnail.image = img_not_available

    def select_video_through_button_press(self, video_side=LEFT):
        selected_video_filename = select_video_filename()
        self.set_video_thumbnail_based_on_filename(selected_video_filename, video_side)

    def set_next_button_state(self):
        if self.left_video_selected and self.right_video_selected:
            self.next_button.configure(state=NORMAL)

    def start(self):
        if does_tmp_file_exist_basename(VIDEOS_SELECTED_TMP_FILENAME):
            video_filenames = read_tmp_file(VIDEOS_SELECTED_TMP_FILENAME)
            video_filenames = ast.literal_eval(video_filenames)
            self.set_video_thumbnail_based_on_filename(video_filenames[LEFT], LEFT)
            self.set_video_thumbnail_based_on_filename(video_filenames[RIGHT], RIGHT)

    def stop(self):
        video_filenames_used = {LEFT: self.left_video_filename, RIGHT: self.right_video_filename}
        write_to_tmp_file(VIDEOS_SELECTED_TMP_FILENAME, str(video_filenames_used))

    def set_video_thumbnail_based_on_filename(self, video_filename, video_side=LEFT):
        if os.path.isfile(os.path.join(os.path.dirname(video_filename), os.path.basename(video_filename))):
            vc_object = cv2.VideoCapture(video_filename)
            _, img = vc_object.read()
            vc_object.release()

            img = cv2_bgr_image_to_tkinter_with_resize(img, VIDEO_PREVIEW_WIDTH, VIDEO_PREVIEW_HEIGHT)
            self.update_ui(video_filename, img, True, video_side)

    def update_ui(self, filename, img, video_selected, video_side=LEFT):
        if video_selected and video_side == LEFT:
            self.left_video_selected = True
            self.left_video_filename = filename
            self.left_video_filename_preview_label.config(text=os.path.basename(os.path.normpath(filename)))
            self.set_next_button_state()

            self.left_video_thumbnail.configure(image=img)
            self.left_video_thumbnail.image = img
        elif video_selected and video_side == RIGHT:
            self.right_video_selected = True
            self.right_video_filename = filename
            self.right_video_filename_preview_label.config(text=os.path.basename(os.path.normpath(filename)))
            self.set_next_button_state()

            self.right_video_thumbnail.configure(image=img)
            self.right_video_thumbnail.image = img


def select_video_filename():
    filename = filedialog.askopenfilename(initialdir=os.path.dirname(ROOT_DIR), title="Select left video",
                                          filetypes=[("MKV files", "*.mkv"),
                                                     ("AVI files", "*.avi"),
                                                     ("MP4 files", "*mp4")])
    return filename
