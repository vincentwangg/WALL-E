import os
import subprocess

from definitions import ROOT_DIR


def main():
    os.chdir(ROOT_DIR)
    subprocess.call(["blender", "--python", "mapping_3d/blender_pulse_mapper.py"])


if __name__ == '__main__':
    main()
