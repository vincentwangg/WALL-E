import datetime
import cv2
from Tkinter import Canvas, Frame, Scrollbar, Label, VERTICAL, CENTER, Button, PhotoImage
from math import ceil

from gui.pipeline1.sr_no_frames_found_screen import SrNoFramesFoundScreen
from gui.pipeline1.utilities.constants import WINDOW_WIDTH, WINDOW_HEIGHT, SCREENS_REL_X, LEFT, RIGHT, \
    FRAME_NUM_LABEL, SR_MAP_LABEL, SR_FRAME_SELECTION_TITLE
from gui.widgets.gui_base_frame import GuiBaseFrame
from gui.widgets.header1_label import Header1Label
from gui.widgets.p_label import PLabel
from gui.widgets.checkerboard_select_button import CheckerboardSelectButton
from utils_general.image_converter import cv2_gray_image_to_tkinter_with_resize
from utilities.constants import VIDEO_SR_SELECT_PREVIEW_WIDTH, VIDEO_PREVIEW_HEIGHT
from stereo_rectification.sr_map_gen import select_frames_for_stereo_rectification

RESULTS_PER_PAGE = 10

class SrCheckerBoardSelection(GuiBaseFrame):
    def __init__(self, parent, controller, **kw):
        GuiBaseFrame.__init__(self, parent, controller, **kw)

    def init_widgets(self):
        self.content_wrapper = Frame(self)
        self.screen_title = Header1Label(self.content_wrapper, text=SR_FRAME_SELECTION_TITLE)
        self.screen_description = PLabel(self.content_wrapper, text="Please select frames that have a satisfactory "
                                                                    "checkerboard result.")
        self.next_button = Button(self.content_wrapper, text="Next",
                                  command=lambda: self.on_next_button())

    def add_widgets_to_frame(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.screen_title.grid(row=0, column=0, columnspan=3)
        self.screen_description.grid(row=1, columnspan=3)
        self.content_wrapper.place(relx=SCREENS_REL_X, rely=0.48, anchor=CENTER)
        self.next_button.grid(row=4, column=1)

    def on_show_frame(self):
        self.canvas_wrappers = []
        self.canvases = []
        self.page_num = 0

        if len(self.controller.builder.checkerboard_frames) == 0:
            self.controller.show_frame(SrNoFramesFoundScreen)
        else:
            pages = int(ceil(len(self.controller.builder.checkerboard_frames) / 10.0))
            for page in range(0, pages):
                canvas_wrapper = Frame(self.content_wrapper, borderwidth="1", relief="solid")
                canvas = Canvas(canvas_wrapper, width=int(WINDOW_WIDTH * 7 / 8), height=(WINDOW_HEIGHT * 2 / 3))
                scroll_bar = Scrollbar(canvas_wrapper, orient=VERTICAL, command=canvas.yview)
                results_list_frame = Frame(canvas)

                canvas.configure(yscrollcommand=scroll_bar.set)
                canvas.create_window(0, 0, window=results_list_frame)
                canvas.bind_all("<Up>", self.on_up_key)
                canvas.bind_all("<Down>", self.on_down_key)
                canvas.bind_all("<Left>", self.on_left_key)
                canvas.bind_all("<Right>", self.on_right_key)

                canvas.grid(row=0, column=0, sticky="nsew")
                scroll_bar.grid(row=0, column=1, sticky="ns")
                canvas_wrapper.grid(row=2, column=0, columnspan=3, sticky="nsew")

                select_buttons_on_page = []

                for row in range(0, RESULTS_PER_PAGE):

                    result_num = page * RESULTS_PER_PAGE + row
                    if result_num < len(self.controller.builder.checkerboard_frames):
                        frame_num = self.controller.builder.checkerboard_frames[result_num].left_image_num

                        result_entry = Frame(results_list_frame, borderwidth="1", relief="solid")
                        description = PLabel(result_entry, text="Frame #" + str(int(frame_num)) +
                                                                ", Time: " +
                                                                str(datetime.timedelta(seconds=frame_num / 30)))
                        preview_wrapper = Frame(result_entry)
                        
                        left_image_obj = self.convert_image(self.controller.builder.checkerboard_frames[result_num].left_image)
                        right_image_obj = self.convert_image(self.controller.builder.checkerboard_frames[result_num].right_image)

                        left_video_preview = Label(preview_wrapper, image=left_image_obj)
                        left_video_preview.image = left_image_obj
                        right_video_preview = Label(preview_wrapper, image=right_image_obj)
                        right_video_preview.image = right_image_obj

                        select_button = CheckerboardSelectButton(preview_wrapper, self.controller,
                                                       checkerboard=self.controller.builder.checkerboard_frames[result_num], text="Select")

                        select_buttons_on_page.append(select_button)

                        description.pack()
                        left_video_preview.grid(row=row, column=0)
                        right_video_preview.grid(row=row, column=1)
                        select_button.grid(row=row, column=2)
                        preview_wrapper.pack()
                        result_entry.pack()

                for i in range(0, len(select_buttons_on_page)):
                    select_buttons_on_page[i].configure(command=select_buttons_on_page[i].choose_checkerboard)

                self.master.update_idletasks()
                canvas.config(scrollregion=canvas.bbox("all"))
                canvas.yview_moveto(0)
                self.canvas_wrappers.append(canvas_wrapper)
                self.canvases.append(canvas)

            self.prev_result_page = Button(self.content_wrapper, text="<",
                                           command=lambda: self.prev_page_command())
            self.page_info_label = PLabel(self.content_wrapper,
                                          text=get_page_info_label_message(self.page_num,
                                                                           len(self.canvases),
                                                                           RESULTS_PER_PAGE))
            self.next_result_page = Button(self.content_wrapper, text=">",
                                           command=lambda: self.next_page_command())

            self.prev_result_page.grid(row=3, column=0)
            self.page_info_label.grid(row=3, column=1)
            self.next_result_page.grid(row=3, column=2)
            self.canvas_wrappers[self.page_num].tkraise()

    def update_frame(self, data):
        pass

    def on_hide_frame(self):
        pass

    def on_up_key(self, event):
        self.canvases[self.page_num].yview_scroll(-7, 'units')

    def on_down_key(self, event):
        self.canvases[self.page_num].yview_scroll(7, 'units')

    def on_left_key(self, event):
        self.prev_page_command()

    def on_right_key(self, event):
        self.next_page_command()

    def prev_page_command(self):
        if self.page_num > 0:
            self.page_num -= 1
            self.canvas_wrappers[self.page_num].tkraise()
            self.page_info_label.configure(text=get_page_info_label_message(self.page_num,
                                                                       len(self.canvases),
                                                                       RESULTS_PER_PAGE))

    def next_page_command(self):
        if self.page_num < len(self.canvas_wrappers) - 1:
            self.page_num += 1
            self.canvas_wrappers[self.page_num].tkraise()
            self.page_info_label.configure(text=get_page_info_label_message(self.page_num,
                                                                       len(self.canvases),
                                                                       RESULTS_PER_PAGE))

    def convert_image(self, image):
        return cv2_gray_image_to_tkinter_with_resize(image, VIDEO_SR_SELECT_PREVIEW_WIDTH, VIDEO_PREVIEW_HEIGHT)

    def on_next_button(self):
        if (len(self.controller.builder.chosen_checkerboard_frames) > 0):
            select_frames_for_stereo_rectification(self.controller)
            self.controller.show_next_frame()



def get_page_info_label_message(page_num, total_pages, results_per_page):
    return "".join(["Page ", str(page_num + 1), " of ", str(total_pages), ". Showing ",
                    str(results_per_page), " results per page."])
