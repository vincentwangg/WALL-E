import os

import cv2
import sys
from stereo_rectification.sr_map_gen import undistort


def undistort_video(video_filename, new_file_ext, frame_cap=0):
    new_filename = video_filename[:-4] + "_undistorted" + new_file_ext
    undistorted_video = None
    video = cv2.VideoCapture(video_filename)
    while not video.isOpened():
        video = cv2.VideoCapture(video_filename)
        cv2.waitKey(1000)
        print("Wait for the header")

    pos_frame = video.get(cv2.CAP_PROP_POS_FRAMES)
    i = 0
    attempts_to_read_frame = 0
    while True and (i < frame_cap or frame_cap == 0):
        flag, frame = video.read()
        if flag:
            # The frame is ready and already captured
            # cv2.imshow('video', frame)
            pos_frame = video.get(cv2.CAP_PROP_POS_FRAMES)
            undistorted_frame = undistort(frame)

            if undistorted_video is None:
                height, width, layers = undistorted_frame.shape
                fourcc = cv2.VideoWriter_fourcc(*'FFV1')
                try:
                    os.remove(new_filename)
                except OSError:
                    pass
                undistorted_video = cv2.VideoWriter(new_filename, fourcc, 30.0, (width, height))

            undistorted_video.write(undistorted_frame)
            i = i + 1
            # print str(pos_frame) + " frames"
        else:
            # The next frame is not ready, so we try to read it again
            video.set(cv2.CAP_PROP_POS_FRAMES, pos_frame - 1)
            # print "frame is not ready"
            # It is better to wait for a while for the next frame to be ready
            cv2.waitKey(1000)
            attempts_to_read_frame = attempts_to_read_frame + 1
            if attempts_to_read_frame > 10:
                break

        if video.get(cv2.CAP_PROP_POS_FRAMES) == video.get(cv2.CAP_PROP_FRAME_COUNT):
            # If the number of captured frames is equal to the total number of frames, we stop
            break
    undistorted_video.release()
    cv2.destroyAllWindows()
    return new_filename


if __name__ == '__main__':
    print(sys.argv)
    if len(sys.argv) != 2:
        print("Please provide one argument (filename of video)")

    print("Undistorting video: " + sys.argv[1])
    new_filename = undistort_video(sys.argv[1], ".mkv")
    print("Video undistorted. New video name: " + new_filename)
