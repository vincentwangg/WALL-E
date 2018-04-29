import cv2


FRAME_NUM = 40890
OFFSET = 10

video = cv2.VideoCapture('../../videos/EGD_left.mkv')
video.set(cv2.CAP_PROP_POS_FRAMES,FRAME_NUM)
success, image = video.read()
h, w, _ = image.shape
image = image[0:h-40, :]
cv2.imshow("image_l", image)

cv2.imwrite(str(FRAME_NUM)+'_ostracod_left.jpg', image)

video2 = cv2.VideoCapture('../../videos/EGD_right.mkv')
video2.set(cv2.CAP_PROP_POS_FRAMES, FRAME_NUM + OFFSET)
success2, image2 = video2.read()
image2 = cv2.flip(image2, -1)


image2 = image2[40:h, :]
cv2.imshow("image_r", image2)
cv2.waitKey(0)
cv2.imwrite(str(FRAME_NUM)+'_ostracod_right.jpg', image2)