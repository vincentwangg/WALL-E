import cv2

def main():
    setpos = 964
    vc_l = cv2.VideoCapture("../Flat_leftview.mkv") # 196, flat: 964
    vc_r = cv2.VideoCapture("../Flat_rightview.mkv") # 209 flat: 977
    count = 964
    vc_l.set(cv2.CAP_PROP_POS_FRAMES,setpos)
    vc_r.set(cv2.CAP_PROP_POS_FRAMES, setpos)
    video = vc_r
    ret, frame = video.read()
    print ret
    while ret:
        cv2.flip(frame,-1,frame)
        count +=1
        print count
        cv2.imshow("image", frame)
        cv2.waitKey(0)
        ret, frame = video.read()

main()