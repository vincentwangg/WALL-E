import errno
import os

from definitions import TMP_FOLDER_PATH


def create_tmp_dir_if_does_not_exist():
    try:
        os.makedirs(TMP_FOLDER_PATH)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def get_tmp_file_path(file_basename):
    return os.path.join(TMP_FOLDER_PATH, file_basename)


def does_tmp_file_exist_basename(basename):
    return os.path.isfile(get_tmp_file_path(basename))


def does_tmp_file_exist(filename):
    return os.path.isfile(filename)


def write_to_tmp_file(filename, contents):
    create_tmp_dir_if_does_not_exist()
    with open(os.path.join(TMP_FOLDER_PATH, filename), mode="w") as file:
        file.write(contents)


def read_tmp_file(filename):
    with open(os.path.join(TMP_FOLDER_PATH, filename), mode="r") as file:
        return file.read()
