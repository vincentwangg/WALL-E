# Ostracod Model

class Ostracod:
    def __init__(self, location, area, brightness):
        self.location = location     # x, y coordinates
        self.area = area              # area of the contour
        self.brightness = brightness         # 0-255
        self.matches = []           # indexes of another ostracod in a corresponding stereo frame, match value