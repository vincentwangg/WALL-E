import bpy
import sys
import argparse
import os
import ast

import math

fps_value = 30
rotation_toward_pos_z = (0, math.radians(180), math.radians(270))


def main(points_filename):
    delete_all_objects()
    set_fps(fps_value)

    # Plot ostracod points
    points = get_points_from_file(points_filename)

    for frame_num in points:
        plot_points_from_frame(points, frame_num)

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


def set_fps(new_fps):
    bpy.context.scene.render.fps = new_fps


def get_points_from_file(points_filename):
    # Future iterations file syntax:
    #   Dictionary with a frame number matched to a list of xyz point
    #   coordinates.
    #
    #   Example of a points.txt:
    #                           
    #       Frame 1 points      {1: [[[1, 2, 3], 0.2], [[2, 3, 4], 0.4]],
    #       Frame 2 points       2: [[[2, 2, 3], 0.8], [[3, 3, 4], 0.1]],
    #       Frame 3 points       3: [[[2, 3, 3], 0.3], [[3, 4, 4], 0.2]]}
    #
    #       Full string (for ctrl-c): {1: [[[0, 2, 0], 0.2], [[2, 3, 4], 0.4]], 2: [[[2, 2, 3], 0.8], [[3, 3, 4], 0.1]], 3: [[[2, 3, 3], 0.3], [[3, 4, 4], 0.2]]}
    #   
    #   One can see from the points.txt example that as time moves on,
    #   the points move one unit positively in the x direction, then
    #   the y direction.

    points_file = open(points_filename, "r")
    if points_file.mode == 'r':
        points_string = points_file.read()
        return ast.literal_eval(points_string)
    else:
        sys.exit("File " + points_filename + " couldn't be read.")


def plot_points_from_frame(points, frame_num):
    for point, radius in points[frame_num]:
        plot_point(point, radius, frame_num)


# Coordinates should be in format [x, y, z]
def plot_point(coordinate, radius, frame_num):
    bpy.ops.mesh.primitive_uv_sphere_add(size=radius, location=coordinate)
    obj = bpy.context.active_object
    obj.color = (255, 255, 255, 1)

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


if __name__ == '__main__':
    argv = sys.argv
    if "--" not in argv:
        argv = []  # as if no args are passed
    else:
        argv = argv[argv.index("--") + 1:]  # get all args after "--"

    if len(argv) == 1:
        main(argv[0])
    else:
        print("Incorrect number of arguments. "
              + "Usage: blender --background "
              + "--python " + os.path.basename(__file__) + " "
              + "-- [points filename]")
