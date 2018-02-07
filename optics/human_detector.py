import cv2
import imutils
import time

class HumanDetector:


    def __init__(self):
        # initialize detector
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    def detect(self, image, winStride=(4,4), padding=(6,6), scale=1.05):
        """
        Detects humans in the given image.

        :param image:
        :return: tuple bounding boxes and weights
        """
        before = time.time()
        image = imutils.resize(image, width=min(350, image.shape[1]))
        boxes = self.hog.detectMultiScale(image, winStride=winStride, padding=padding, scale=scale)
        after = time.time()
        print("took {}s to find bounding boxes and weights {}".format(after - before, boxes))
        return boxes
