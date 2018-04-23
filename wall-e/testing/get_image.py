import cv2

video = cv2.VideoCapture('../../EGD_left.mkv')
video.set(cv2.CAP_PROP_POS_FRAMES,50399)
success, image = video.read()
cv2.imshow("image", image)
cv2.waitKey(0)
cv2.imwrite('ostracod.jpg',image)