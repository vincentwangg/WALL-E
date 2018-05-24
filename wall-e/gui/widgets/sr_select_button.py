# Button that holds data to use for later
from Tkinter import Button

from stereo_rectification.sr_map_gen import write_sr_map_to_file


class SrSelectButton(Button):
    def __init__(self, master, controller, sr_map, **kw):
        Button.__init__(self, master, **kw)
        self.master = master
        self.controller = controller
        self.sr_map = sr_map

    def use_sr_map(self):
        write_sr_map_to_file(self.sr_map)
        self.controller.sr_map = self.sr_map
        self.controller.show_next_frame()
