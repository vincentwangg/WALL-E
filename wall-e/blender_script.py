import os
from definitions import ROOT_DIR
import subprocess


def main():
    os.chdir(ROOT_DIR)
    subprocess.check_call(["blender", "--python", "mapping_3d/blender_pulse_mapper.py", "--"])


if __name__ == '__main__':
    main()
