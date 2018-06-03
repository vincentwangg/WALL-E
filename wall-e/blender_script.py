import os
import subprocess
import sys

from definitions import ROOT_DIR


def main():
    os.chdir(ROOT_DIR)
    out = subprocess.check_output(["whereis", "blender"])
    if len(out.split()) < 2:
        sys.exit("You must install blender!")
    blender_path = out.split()[1]
    subprocess.call([blender_path, "--python", "mapping_3d/blender_pulse_mapper.py"])


if __name__ == '__main__':
    main()
