# Create (x,y,z) object points for all intersections on checkerboard grid
objp = np.zeros((5 * 7, 3), np.float32)
objp[:, :2] = np.mgrid[0:7, 0:5].T.reshape(-1, 2)

# Create empty arrays for oject points and image points from each image
objpoints = []
imgpoints = []

# List image files
# images = glob.glob('/home/trinityrael/EGD_video_analysis/Right/Right_calibration_photos/*.jpg')

# for file in images:
# l = cv2.VideoCapture("../Left.ASF")
# l.set(1, 700)
# succ, img = l.read()
# cv2.imwrite('image.jpg',img)
img = cv2.imread('image.jpg')
cv2.imshow('checker board.jpg',img)
# cv2.waitKey(0)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


ret, corners = cv2.findChessboardCorners(gray,(5,4))
print ret,corners

# If found, add object points to objpoints array, and add image points (after refining them) to imgpoints array
if ret == True:
    print 'ret is true'
    objpoints.append(objp)
    cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)  # refine image points
    imgpoints.append(corners)

    # Draw and display the corners
    cv2.drawChessboardCorners(img, (9, 7), corners, ret)
    cv2.imshow('Image with Corner Points', img)
    cv2.waitKey(0)
print 'yo'
cv2.destroyAllWindows()
'''
frames = glob.glob('/home/trinityrael/EGD_video_analysis/Right/EGD_upsidedown(frames_ffmpeg)')

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

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
