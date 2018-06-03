import os
import subprocess

from definitions import ROOT_DIR


def main():
    os.chdir(ROOT_DIR)
    out = subprocess.check_output(["whereis", "blender"])
    blender_path = out.split()[1]
    subprocess.call([blender_path, "--python", "mapping_3d/blender_pulse_mapper.py"])


if __name__ == '__main__':
    main()
