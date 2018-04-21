# Ostracod Model

class Ostracod:
    def __init__(self, location, area, brightness, matched=False):
        self.location = location     # x, y coordinates
        self.area = area              # area of the contour
        self.brightness = brightness         # 0-255
        self.matched = matched           # coordinates of another ostracod in a corresponding stereo frame