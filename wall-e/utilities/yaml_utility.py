import cv2


def read_from_yml(fs, name):
    val = fs.getNode(name).mat()
    return val


# The first time you write to a file w needs to be 1
def save_to_yml(file, name, object, w=0):
    if w:
        fs = cv2.FileStorage(file, flags=cv2.FILE_STORAGE_WRITE)
    else:
        fs = cv2.FileStorage(file, flags=cv2.FILE_STORAGE_APPEND)
    fs.write(name, object)
    fs.release()
