import cv2
from gui.gui_base_frame import GuiBaseFrame
from tkinter import *
from tkinter import filedialog
from definitions import *
from PIL import ImageTk, Image

THUMBNAIL_HEIGHT = 480
THUMBNAIL_WIDTH = 640

INSTRUCTION_ROW = 0
THUMBNAIL_ROW = 1
FILENAME_PREVIEW_ROW = 2
CHOOSE_VIDEO_BUTTON_ROW = 3
NEXT_BUTTON_ROW = 4

LEFT_VIDEO_THUMBNAIL_COL = 0
RIGHT_VIDEO_THUMBNAIL_COL = 2


class VideoSelectionScreen(GuiBaseFrame):
    def __init__(self, parent, controller):
        GuiBaseFrame.__init__(self, parent, controller)

    def setup_widgets(self):
        self.configure(bg="white")

        self.left_video_selected = False
        self.right_video_selected = False

        self.left_video_filename = None
        self.right_video_filename = None

        self.instruction_label = Label(self, text="Please choose your left and right video files.")
        self.left_video_filename_preview_label = Label(self, text="No Video Selected")
        self.left_video_button = Button(self, text="Choose Left Video",
                                        command=lambda: self.set_left_video_thumbnail())
        self.right_video_filename_preview_label = Label(self, text="No Video Selected")
        self.right_video_button = Button(self, text="Choose Right Video",
                                         command=lambda: self.set_right_video_thumbnail())
        self.next_button = Button(self, text="Next", state=DISABLED,
                                  command=lambda: self.controller.set_video_filenames(self.left_video_filename,
                                                                                      self.right_video_filename))

        self.add_img_previews()

        self.instruction_label.grid(row=INSTRUCTION_ROW, column=0, columnspan=3)
        self.left_video_thumbnail.grid(row=THUMBNAIL_ROW, column=0)
        self.left_video_filename_preview_label.grid(row=FILENAME_PREVIEW_ROW, column=0)
        self.left_video_button.grid(row=CHOOSE_VIDEO_BUTTON_ROW, column=0)
        self.right_video_thumbnail.grid(row=THUMBNAIL_ROW, column=2)
        self.right_video_filename_preview_label.grid(row=FILENAME_PREVIEW_ROW, column=2)
        self.right_video_button.grid(row=CHOOSE_VIDEO_BUTTON_ROW, column=2)
        self.next_button.grid(row=NEXT_BUTTON_ROW, column=0, columnspan=3)

    def add_img_previews(self):
        img_not_available = cv2.imread(get_asset_filename(IMG_NOT_AVAILABLE_FILENAME))
        img_not_available = cv2.cvtColor(img_not_available, cv2.COLOR_BGR2RGB)
        img_not_available = Image.fromarray(img_not_available)
        img_not_available = img_not_available.resize((THUMBNAIL_WIDTH, THUMBNAIL_WIDTH), Image.ANTIALIAS)
        img_not_available = ImageTk.PhotoImage(img_not_available)

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

            self.left_video_thumbnail = Label(self, image=img)
            self.left_video_thumbnail.image = img
            self.left_video_thumbnail.grid(row=1, column=0)

    def set_right_video_thumbnail(self):
        video_selected, img, filename = get_video_thumbnail()

        if video_selected:
            self.right_video_selected = True
            self.right_video_filename = filename
            self.right_video_filename_preview_label.config(text=os.path.basename(os.path.normpath(filename)))
            self.set_next_button_state()

            self.right_video_thumbnail = Label(self, image=img)
            self.right_video_thumbnail.image = img
            self.right_video_thumbnail.grid(row=1, column=2)

    def set_next_button_state(self):
        if self.left_video_selected and self.right_video_selected:
            self.next_button.configure(state=NORMAL)


def get_video_thumbnail():
    video_filename = select_video_filename()

    if len(video_filename) > 0:
        vc_object = cv2.VideoCapture(video_filename)
        vc_object.set(cv2.CAP_PROP_POS_FRAMES, 0)
        _, img = vc_object.read()
        vc_object.release()

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        img = img.resize((THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)
        return True, img, video_filename
    return False, None, None


def select_video_filename():
    filename = filedialog.askopenfilename(initialdir=os.path.dirname(ROOT_DIR), title="Select left video",
                                          filetypes=[("MKV files", "*.mkv"),
                                                     ("AVI files", "*.avi"),
                                                     ("MP4 files", "*mp4")])
    return filename
