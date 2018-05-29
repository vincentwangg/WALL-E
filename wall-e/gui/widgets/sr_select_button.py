# Button that holds data to use for later
from Tkinter import Button


class SrSelectButton(Button):
    def __init__(self, master, controller, sr_map, **kw):
        Button.__init__(self, master, **kw)
        self.master = master
        self.controller = controller
        self.sr_map = sr_map

    def use_sr_map(self):
        self.sr_map.write_to_yml_file()
        self.controller.sr_map = self.sr_map
        self.controller.show_next_frame()
