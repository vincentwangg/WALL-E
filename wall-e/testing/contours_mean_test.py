import numpy as np
import cv2
# USAGE: python2 contours.py -i"./ostracod.png" -b120 -w120
# The above params work pretty well
black = 120
white = 100

im = cv2.imread('./ostracod.png')

imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)

ret,thresh = cv2.threshold(imgray,black,white,cv2.THRESH_BINARY)
imgray2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

for contour in contours:
    mask = np.zeros(imgray.shape, np.uint8)
    cv2.drawContours(mask, [contour], 0, 255, -1)
    mean_val = cv2.mean(imgray,mask = mask)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(imgray, mask = mask)
    imgray2[max_loc[1], max_loc[0]] = 0
    cv2.drawContours(imgray2, [contour], 0, (0, 255, 255), 1)
    cv2.imshow("im", imgray2)
    cv2.waitKey(0)
    if cv2.contourArea(contour) > 0:
        M = cv2.moments(contour)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        # im[cY, cX] = (255, 0, 0)




# ret,thresh = cv2.threshold(imgray,black,white,cv2.THRESH_BINARY)
# imgray2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
# cv2.imshow("imgray",imgray)
# cv2.waitKey(0)
# cv2.drawContours(im,contours,2,(0,255,255), -1)
# print "X\tY\tArea\tMinI\tMaxI\tMeanI"
# for c in contours:
#     # compute the center of the contour
#     if cv2.contourArea(c) > 0:
#         M = cv2.moments(c)
#         cX = int(M["m10"] / M["m00"])
#         cY = int(M["m01"] / M["m00"])
#         mask = np.zeros(imgray.shape,np.uint8)
#         cv2.drawContours(mask,[c],0,255,-1)
#         cv2.imshow("mask", mask)
#         cv2.waitKey(0)
#         mean_val = cv2.mean(imgray,mask = mask)
#         min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(imgray,mask = mask)
#         print cX,"\t",cY,"\t",cv2.contourArea(c),"\t",min_val,"\t",max_val,"\t",mean_val[0]
#         im[cY,cX] = 0
#
#
# cv2.imshow("Contours", im)
# cv2.waitKey(0)

