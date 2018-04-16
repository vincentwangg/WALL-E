import bpy
import sys
import argparse
import os
import ast

fps_value = 30

def main(points_filename):
    delete_all_objects()
    set_fps(fps_value)
    points = get_points_from_file(points_filename)

    for frame_num in points:
        plot_points_from_frame(points, frame_num)

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
    #       Frame 1 points      {1: [[1, 2, 3], [2, 3, 4]],
    #       Frame 2 points       2: [[2, 2, 3], [3, 3, 4]],
    #       Frame 3 points       3: [[2, 3, 3], [3, 4, 4]]}
    #
    #       Full string (for ctrl-c): {1: [[1, 2, 3], [2, 3, 4]], 2: [[2, 2, 3], [3, 3, 4]], 3: [[2, 3, 3], [3, 4, 4]]}
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
    for point in points[frame_num]:
        plot_point(point, frame_num)

        
# Coordinates should be in format [x, y, z]
def plot_point(coordinate, frame_num):
    bpy.ops.mesh.primitive_ico_sphere_add(size=0.5, location=coordinate)
    obj = bpy.context.active_object

    obj.keyframe_insert('hide', frame=frame_num)
    obj.keyframe_insert('hide_render', frame=frame_num)
    
    # Hide object
    obj.hide = True
    obj.hide_render = True
    
    # Hide object in the frames before and after
    obj.keyframe_insert('hide', frame=frame_num-1)
    obj.keyframe_insert('hide_render', frame=frame_num-1)
    obj.keyframe_insert('hide', frame=frame_num+1)
    obj.keyframe_insert('hide_render', frame=frame_num+1)

    
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
