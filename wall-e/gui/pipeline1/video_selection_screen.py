import cv2
from tkinter import *
from tkinter import filedialog
from definitions import *
from gui.gui_base_frame import GuiBaseFrame
from gui.pipeline1.constants import VIDEO_WIDTH, VIDEO_HEIGHT
from gui.pipeline1.sr_frame_suggestion_intro_screen import SrFrameSuggestionIntroScreen
from gui.pipeline1.video_scan_screen import VideoScanScreen
from gui.widgets.header1_label import Header1Label
from gui.widgets.p_label import PLabel
from utilities.image_converter import cv2_bgr_image_to_tkinter_with_resize

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
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.left_video_selected = False
        self.right_video_selected = False

        self.left_video_filename = None
        self.right_video_filename = None

        self.screen_title_label = Header1Label(self, text="Video Selection")
        self.instruction_label = PLabel(self, text="Please choose your left and right video files.")
        self.left_video_filename_preview_label = PLabel(self, text="No Video Selected")
        self.left_video_button = Button(self, text="Choose Left Video",
                                        command=lambda: self.set_left_video_thumbnail())
        self.right_video_filename_preview_label = PLabel(self, text="No Video Selected")
        self.right_video_button = Button(self, text="Choose Right Video",
                                         command=lambda: self.set_right_video_thumbnail())
        self.next_button = Button(self, text="Next", state=DISABLED,
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

    def next_screen(self):
        self.controller.set_video_filenames(self.left_video_filename, self.right_video_filename)
        self.controller.show_frame(VideoScanScreen)

    def add_img_previews(self):
        img_not_available = cv2.imread(get_asset_filename(IMG_NOT_AVAILABLE_FILENAME))
        img_not_available = cv2_bgr_image_to_tkinter_with_resize(img_not_available, VIDEO_WIDTH, VIDEO_HEIGHT)

        self.left_video_thumbnail = Label(self, image=img_not_available)
        self.left_video_thumbnail.image = img_not_available
        self.right_video_thumbnail = Label(self, image=img_not_available)
        self.right_video_thumbnail.image = img_not_available

    def set_left_video_thumbnail(self):
        video_selected, img, filename = get_video_thumbnail()

        if video_selected:
            self.left_video_selected = True
            self.left_video_filename = filename
            self.left_video_filename_preview_label.config(text=os.path.basename(os.path.normpath(filename)))
            self.set_next_button_state()

            self.left_video_thumbnail.configure(image=img)
            self.left_video_thumbnail.image = img

    def set_right_video_thumbnail(self):
        video_selected, img, filename = get_video_thumbnail()

        if video_selected:
            self.right_video_selected = True
            self.right_video_filename = filename
            self.right_video_filename_preview_label.config(text=os.path.basename(os.path.normpath(filename)))
            self.set_next_button_state()

            self.right_video_thumbnail.configure(image=img)
            self.right_video_thumbnail.image = img

    def set_next_button_state(self):
        if self.left_video_selected and self.right_video_selected:
            self.next_button.configure(state=NORMAL)

    def start(self):
        pass

    def stop(self):
        pass


def get_video_thumbnail():
    video_filename = select_video_filename()

    if len(video_filename) > 0:
        vc_object = cv2.VideoCapture(video_filename)
        _, img = vc_object.read()
        vc_object.release()

        img = cv2_bgr_image_to_tkinter_with_resize(img, VIDEO_WIDTH, VIDEO_HEIGHT)
        return True, img, video_filename
    return False, None, None


def select_video_filename():
    filename = filedialog.askopenfilename(initialdir=os.path.dirname(ROOT_DIR), title="Select left video",
                                          filetypes=[("MKV files", "*.mkv"),
                                                     ("AVI files", "*.avi"),
                                                     ("MP4 files", "*mp4")])
    return filename
