import cv2

class Camera:
    def __init__(self, baseline):
        self.focal_length = self.get_focal_length()
        self.baseline = baseline


    def get_focal_length(self):
        print "stub"