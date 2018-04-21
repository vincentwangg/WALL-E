# Ostracod Model

class ostracod:
    def __init__(self):
        self.location = []      # x, y, z coordinates
        self.area               # area of the contour
        self.brightness         # 0-255
        self.matched            # coordinates of another ostracod in a corresponding stereo frame