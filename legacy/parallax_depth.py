# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import numpy as np

#x values from right camera
xR = np.array((371, 361, 364, 363))

#x values from left camera
xL = np.array((583, 573, 577, 578))

#find distance from optical center and convert pixels to mm
xR = (xR-320)*(4.8/640)
xL = (xL-320)*(4.8/640)

X = np.column_stack((xL,xR))

print X

#xL - xR = disparity
X = [(x - y) for (x,y) in X]

print X

#focal length in milimeters
f = 3.7

#distance between cameras in milimeters
d = 215.9

Z = []
print 'Depth in meters:'

for item in X:
    #equation for distance
    z = f*d/(item)
    
    #convert to meters
    zm = z/1000
    print zm 
    
    Z.append(z)
print Z

import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

YR = np.array((217, 186, 159, 346))
YL = np.array((254, 221, 194, 166))

XL = []
L = np.column_stack((xL,Z))
for (x,y) in L:
    #find X values at distance Z
    theta = math.atan(x/f)
    Xl = [int(math.tan(theta)*y)]
    XL.append(Xl)
print XL

fig = plt.figure()
ax = Axes3D(fig)
ax.scatter(XL, Z, YL, zdir='z', s=20, c='b', depthshade=True)
print (XL,YL,Z)

XR = []
R = np.column_stack((xR,Z))
for (x,y) in R:
    #find X values at distance Z
    theta = math.atan(x/f),
    Xr = [int(math.tan(theta)*y)]
    XR.append(Xr)
print XR

fig = plt.figure()
ax = Axes3D(fig)
ax.scatter(XR, Z, YR, zdir='z', s=20, c='b', depthshade=True)
print (XR,YR,Z)
