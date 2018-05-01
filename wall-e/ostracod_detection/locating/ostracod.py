# Ostracod Model

class Ostracod:
    def __init__(self, location, area, brightness):
        self.location = location            # x, y coordinates
        self.area = area                    # area of the contour
        self.brightness = brightness        # 0-255
        self.matches = []                   # indexes of another ostracod in a corresponding stereo frame, match value
        self.distance_from_mean = 0         # x distance away from mean x coordinate
                                                # (this gets updated in locator.get_ostracods())
