import cv2

class Camera:
    def __init__(self, baseline, focal_length=None):
        if focal_length is None:
            self.focal_length = self.get_focal_length()
        else:
            self.focal_length = focal_length
        self.baseline = baseline


    def get_focal_length(self): # needs video and access to sr_map
        return 3.7
