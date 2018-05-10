import bpy
import sys
import argparse
import os
import math


fps_value = 30
rotation_toward_pos_z = (0, math.radians(180), math.radians(270))
RGB_MAX_VAL = 255
material_names = set()


def main(points_filename):
    delete_all_objects()
    set_fps(fps_value)

    # Plot ostracod points
    fpd = read_frame_pulse_data_from_file(points_filename)

    for frame_num in fpd.frame_pulse_data.keys():
        for pulse_data in fpd.frame_pulse_data[frame_num]:
            plot_pulse(pulse_data, frame_num)

    # Add camera
    bpy.ops.object.camera_add(rotation=rotation_toward_pos_z)
    bpy.context.scene.camera = bpy.context.active_object

    # Add hemi lamp
    lamp_data = bpy.data.lamps.new(name="Hemi Lamp", type='HEMI')
    lamp_obj = bpy.data.objects.new(name="Hemi Lamp", object_data=lamp_data)
    bpy.context.scene.objects.link(lamp_obj)
    lamp_obj.location = (0, 0, -2)
    lamp_obj.rotation_euler = rotation_toward_pos_z

    deselect_all_objects()

    # Set the current frame back to the beginning
    bpy.context.scene.frame_set(0)

    # Add colors to materials
    generate_material_colors()


def set_fps(new_fps):
    bpy.context.scene.render.fps = new_fps


def plot_pulse(pulse_data, frame_num):
    bpy.ops.mesh.primitive_uv_sphere_add(size=pulse_data.radius, location=pulse_data.xyz_coord)
    obj = bpy.context.active_object

    # Create material with color
    material_name = "{'" + BRIGHTNESS_LABEL + "':" + str(pulse_data.brightness) + "}"
    material_names.add(material_name)
    mat = bpy.data.materials.new(name=material_name)
    obj.data.materials.append(mat)

    obj.keyframe_insert('hide', frame=frame_num)
    obj.keyframe_insert('hide_render', frame=frame_num)

    # Hide object
    obj.hide = True
    obj.hide_render = True

    # Hide object in the frames before and after
    obj.keyframe_insert('hide', frame=frame_num - 1)
    obj.keyframe_insert('hide_render', frame=frame_num - 1)
    obj.keyframe_insert('hide', frame=frame_num + 1)
    obj.keyframe_insert('hide_render', frame=frame_num + 1)


def select_all_objects():
    bpy.ops.object.select_all(action='SELECT')


def deselect_all_objects():
    bpy.ops.object.select_all(action='DESELECT')


def delete_all_objects():
    select_all_objects()
    bpy.ops.object.delete()


def generate_material_colors():
    for name in material_names:
        material_dict = ast.literal_eval(name)
        brightness = material_dict[BRIGHTNESS_LABEL]
        bpy.data.materials[name].diffuse_color = (brightness, brightness, brightness)


if __name__ == '__main__':
    argv = sys.argv
    if "--" not in argv:
        argv = []  # as if no args are passed
    else:
        argv = argv[argv.index("--") + 1:]  # get all args after "--"

    walle_basedir = sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    if walle_basedir not in sys.path:
        sys.path.append(walle_basedir)

    from mapping_3d.pulse_data import *

    if len(argv) == 1:
        main(argv[0])
    else:
        print("Incorrect number of arguments. "
              + "Usage: blender --background "
              + "--python " + os.path.basename(__file__) + " "
              + "-- [points filename]")
