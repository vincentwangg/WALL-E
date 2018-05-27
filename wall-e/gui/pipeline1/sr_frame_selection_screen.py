import datetime
from Tkinter import Canvas, Frame, Scrollbar, Label, VERTICAL, CENTER, Button
from math import ceil

from gui.pipeline1.utilities.constants import WINDOW_WIDTH, WINDOW_HEIGHT, SCREENS_REL_X, LEFT, RIGHT, \
    FRAME_NUM_LABEL, SR_MAP_LABEL
from gui.widgets.gui_base_frame import GuiBaseFrame
from gui.widgets.header1_label import Header1Label
from gui.widgets.p_label import PLabel
from gui.widgets.sr_select_button import SrSelectButton

RESULTS_PER_PAGE = 10


class SrFrameSelection(GuiBaseFrame):
    def __init__(self, parent, controller, **kw):
        GuiBaseFrame.__init__(self, parent, controller, **kw)

    def init_widgets(self):
        self.content_wrapper = Frame(self)
        self.screen_title = Header1Label(self.content_wrapper, text="Stereo Rectification Frame Selection")
        self.screen_description = PLabel(self.content_wrapper, text="Please select a frame that has a satisfactory "
                                                                    "stereo rectification result.")

    def add_widgets_to_frame(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.screen_title.grid(row=0, column=0, columnspan=3)
        self.screen_description.grid(row=1, columnspan=3)
        self.content_wrapper.place(relx=SCREENS_REL_X, rely=0.48, anchor=CENTER)

    def on_show_frame(self):
        self.canvas_wrappers = []
        self.canvases = []
        self.page_num = 0

        pages = int(ceil(len(self.controller.sr_results) / 10.0))
        for page in range(0, pages):
            canvas_wrapper = Frame(self.content_wrapper, borderwidth="1", relief="solid")
            canvas = Canvas(canvas_wrapper, width=int(WINDOW_WIDTH * 7 / 8), height=(WINDOW_HEIGHT * 2 / 3))
            scroll_bar = Scrollbar(canvas_wrapper, orient=VERTICAL, command=canvas.yview)
            results_list_frame = Frame(canvas)

            canvas.configure(yscrollcommand=scroll_bar.set)
            canvas.create_window(0, 0, window=results_list_frame)
            canvas.bind_all("<Up>", self.on_up_key)
            canvas.bind_all("<Down>", self.on_down_key)

            canvas.grid(row=0, column=0, sticky="nsew")
            scroll_bar.grid(row=0, column=1, sticky="ns")
            canvas_wrapper.grid(row=2, column=0, columnspan=3, sticky="nsew")

            select_buttons_on_page = []

            for row in range(0, RESULTS_PER_PAGE):
                result_num = page * RESULTS_PER_PAGE + row
                if result_num < len(self.controller.sr_results):
                    frame_num = self.controller.sr_results[result_num][FRAME_NUM_LABEL]

                    result_entry = Frame(results_list_frame, borderwidth="1", relief="solid")
                    description = PLabel(result_entry, text="Frame #" + str(int(frame_num)) +
                                                            ", Time: " +
                                                            str(datetime.timedelta(seconds=frame_num / 30)))
                    preview_wrapper = Frame(result_entry)
                    left_video_preview = Label(preview_wrapper, image=self.controller.sr_results[result_num][LEFT])
                    right_video_preview = Label(preview_wrapper, image=self.controller.sr_results[result_num][RIGHT])
                    select_button = SrSelectButton(preview_wrapper, self.controller,
                                                   self.controller.sr_results[result_num][SR_MAP_LABEL], text="Select")

                    select_buttons_on_page.append(select_button)

                    description.pack()
                    left_video_preview.grid(row=row, column=0)
                    right_video_preview.grid(row=row, column=1)
                    select_button.grid(row=row, column=2)
                    preview_wrapper.pack()
                    result_entry.pack()

            for i in range(0, len(select_buttons_on_page)):
                select_buttons_on_page[i].configure(command=select_buttons_on_page[i].use_sr_map)

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


def get_page_info_label_message(page_num, total_pages, results_per_page):
    return "".join(["Page ", str(page_num + 1), " of ", str(total_pages), ". Showing ",
                    str(results_per_page), " results per page."])