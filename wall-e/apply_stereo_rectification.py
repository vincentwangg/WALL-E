import cv2
import sys

fourcc = cv2.VideoWriter_fourcc(*'FFV1') ## ffmpeg http://www.fourcc.org/codecs.php

def read(fs,name):
    val = fs.getNode(name).mat()
    return val

# applies map to vc_obj with remap
def apply_rectify_maps(image, map_0, map_1):
    sr_image = cv2.remap(image, map_0, map_1, cv2.INTER_LANCZOS4)
    return sr_image

def stereo_rectify_videos(left_filename,right_filename):
    left_vid = cv2.VideoCapture(left_filename)
    right_vid = cv2.VideoCapture(right_filename)

    sr_left_video = cv2.VideoWriter("stereo_rectified_l.mkv", fourcc, 20.0, (640,478))
    sr_right_video = cv2.VideoWriter("stereo_rectified_r.mkv", fourcc, 20.0, (640,478))
    fs = cv2.FileStorage('sr_maps.yml', cv2.FILE_STORAGE_READ)

    l_sr_map_0 = read(fs, "l_sr_map_0")
    l_sr_map_1 = read(fs, "l_sr_map_1")
    r_sr_map_0 = read(fs, "r_sr_map_0")
    r_sr_map_1 = read(fs, "r_sr_map_1")
    # sys.exit(0)

    # Loop over video footage
    l_success, l_image = left_vid.read()
    r_success, r_image = right_vid.read()

    while l_success and r_success:
        sr_l_image = apply_rectify_maps(l_image, l_sr_map_0, l_sr_map_1) # apply maps
        sr_r_image = apply_rectify_maps(r_image, r_sr_map_0, r_sr_map_1)

        sr_left_video.write(sr_l_image)         # write videos
        sr_right_video.write(sr_r_image)

        l_success, l_image = left_vid.read()    # read next frame
        r_success, r_image = right_vid.read()
    sr_right_video.release()
    sr_left_video.release()


def main():
    left_filename = str(sys.argv[1])
    right_filename = str(sys.argv[2])
    stereo_rectify_videos(left_filename, right_filename)


if __name__ == '__main__':
    main()