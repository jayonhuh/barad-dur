from imutils.object_detection import non_max_suppression
from picamera.array import PiRGBArray
from picamera import PiCamera
from phue import Bridge
import datetime
import time
import cv2
import numpy as np
import imutils

size = (640, 480)
camera = PiCamera()
camera.resolution = size
camera.framerate = 2
rawCapture = PiRGBArray(camera, size=size)

# warm up the camera sensor
time.sleep(0.1)

# initialize detector
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())


# set up the bridge
b = Bridge("10.0.1.35")
b.connect()

frame_num = 0
pick = []

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

    if (frame_num % 1 == 0):
        image = frame.array
        before = time.time()
        image = imutils.resize(image, width=min(300, image.shape[1]))
        (rects, weights) = hog.detectMultiScale(image, winStride=(4, 4), padding=(6,6), scale=1.05)
        # nms
        rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
        pick = rects # non_max_suppression(rects, probs=None, overlapThresh=0.65)
        after = time.time()
        print("took {}s to find bounding boxes {}".format(after - before, rects))

        if len(pick) > 0:
            print("turning on kitchen lights")
            b.set_light(6, 'on', True)
            b.set_light(8, 'on', True)

        else:
            b.set_light(6, 'on', False)
            b.set_light(8, 'on', False)

        for (xA, yA, xB, yB) in pick:
            cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)

        cv2.putText(image, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                            (10, image.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
        cv2.imshow("frame", image)



    rawCapture.truncate(0)
    frame_num += 1
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
