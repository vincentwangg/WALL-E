
"""
Spyder Editor

This is a temporary script file.
"""
import sys

import cv2
import numpy as np
from imread import imread, imsave
import os

# path to folder containing video frames (png files)
folder_input =  'MGL_rightsideup'
path_frames = 'C:\\Users\\Christy\\Documents\\MGL data analysis project\\' + folder_input + '\\'

# output file
file_output = 'mean_brightness_' + folder_input + '.dat'

files = os.listdir(path_frames)
mean_brightness = []

for file in files:
    if file[-4:len(file)]==".png":
     print 'reading image', file

     filename = file[0:-4]
     rgb_image = imread(path_frames + file)

     # mean brightness of the entire frame. 
     # The pixel range of rgb_image can be changed to only look into a specified area of the frame
     mean_brightness_frame = rgb_image.mean()

     mean_brightness.append(mean_brightness_frame)
     
np.savetxt(file_output, mean_brightness, delimiter=',', fmt='%4.4f')

print 'output file: ', file_output


