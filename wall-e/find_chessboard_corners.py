import cv2
import numpy as np

# Create (x,y,z) object points for all intersections on checkerboard grid
objp = np.zeros((5 * 7, 3), np.float32)
objp[:, :2] = np.mgrid[0:7, 0:5].T.reshape(-1, 2)

# Create empty arrays for oject points and image points from each image
objpoints = []
imgpoints = []

# List image files
# images = glob.glob('/home/trinityrael/EGD_video_analysis/Right/Right_calibration_photos/*.jpg')

# for file in images:
r = cv2.VideoCapture("../Right.ASF")
r.set(1, 710)
succ, img_r = r.read()

# cv2.imwrite('image.jpg',img)
cv2.flip(img_r,-1,img_r)
img_l = cv2.imread('image.jpg')
cv2.imshow('left',img_l)
cv2.imshow('right',img_r)

# cv2.waitKey(0)



ret, corners = cv2.findChessboardCorners(img_l,(5,4))
ret_r, corners_r = cv2.findChessboardCorners(img_r,(5,4)) # 7,5 works
print ret_r

# If found, add object points to objpoints array, and add image points (after refining them) to imgpoints array
if ret == True:
    print 'ret is true'
    objpoints.append(objp)
    # cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)  # refine image points
    imgpoints.append(corners)

    # Draw and display the corners
    cv2.drawChessboardCorners(img_l, (5, 4), corners, ret)
    cv2.drawChessboardCorners(img_r, (5, 4), corners, ret)
    cv2.drawChessboardCorners(img_l, (5, 4), corners_r, ret_r)
    cv2.drawChessboardCorners(img_r, (5, 4), corners_r, ret_r)
    cv2.imshow('Image with Corner Points_l', img_l)
    cv2.imshow('Image with Corner Points_r', img_r)
    cv2.waitKey(0)

cv2.destroyAllWindows()

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, img_l.shape[::-1], None, None)

'''
for file in frames:
    img = cv2.imread(file)
    h, w = gray.shape[:2]  # changed image to gray b/c image got error
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
    
    # undistort
    dst = cv2.undistort(img, mtx, dist, None, newcameramtx)

    # crop the image

    x,y,w,h = roi
    dst = dst[y:y+h, x:x+w]
    
    os.chdir('Undistorted_frames')
    cv2.imwrite('Undistortionresult.png',dst)
    cv2.imshow('Undistorted Image',dst)

'''