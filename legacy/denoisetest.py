#!/usr/bin/env python

import numpy as np
import cv2
from matplotlib import pyplot as plt
import matplotlib.image as mpimg

a=70.0	#a is lowest pixel value to keep. below a = 0
b=185.0	#b is highest pixel value. above b = 255
c=0.0	#c is lowest final pixel value
d=255.0	#d is highest final pixel value

img = cv2.imread('Undistortionresult.png')
img2 = cv2.imread('Undistortionresult2.png')

##replace all values > 185 with 255 now transformed
#img[img > 185] = 255
#img2[img2 > 185] = 255
##replace all values < 70 with 0
#img[img < 70] = 0
#img2[img2 < 70] = 0

#linear transform numbers in between ranges
img=(img-a)/(b-img)*(d-c)+c
#img=np.rint(img)
#img[img > 254] = 255
#img[img < 1] = 0



#finds maximum value of pixel level in each image
imgmax = np.amax(img.ravel())
imgmin = np.amin(img.ravel())
img2max = np.amax(img2.ravel())

print imgmin
print imgmax



# Denoising
#dst = cv2.fastNlMeansDenoisingColored(img,None,10,10,7,21)


plt.subplot(221),plt.imshow(img)
plt.subplot(222),plt.hist(img.ravel(),256,[0,256])
plt.subplot(223),plt.imshow(img2)
plt.subplot(224),plt.hist(img2.ravel(),256,[0,256])
plt.show()


#Can collapse to array then reshape into image
#plt.imshow(img.ravel().reshape(480,640,3))
#plt.show()



#print img.shape
#print imgmax
#print img2max
