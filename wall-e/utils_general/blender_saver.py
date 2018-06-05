import cv2

def main():
    dir = "/tmp/"
    frame_nums = 900
    fourcc = cv2.VideoWriter_fourcc(*'FFV1')
    video = cv2.VideoWriter("3d_mapped.mkv", fourcc, 30, (960, 540))

    for num in xrange(1,frame_nums + 1):
        string_num = str(num)
        while len(string_num) < 4:
            string_num = "0" + string_num
        image = cv2.imread(dir + string_num + ".png")
        print image.shape
        video.write(image)

if __name__ == '__main__':
    main()