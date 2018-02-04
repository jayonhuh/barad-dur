import cv2

class MotionDetector:

    def __init__(self, min_area=500):
        self.min_area = min_area

    def detect(self, frame1, frame2):
        """
        Checks for motion between the two provided frames.

        Assumes that frames have already been resized as needed.

        :param frame1:
        :param frame2:
        :return: bounding boxes for detected motion
        """
        # convert our frames to
        gray_frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        gray_frame1 = cv2.GaussianBlur(gray_frame1, (21, 21), 0)
        gray_frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        gray_frame2 = cv2.GaussianBlur(gray_frame2, (21, 21), 0)

        # compute the diff and threshold it
        frame_delta = cv2.absdiff(gray_frame1, gray_frame2)
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]

        # dilate the thresholded image to fill in holes, then find contours
        # on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2)
        (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                     cv2.CHAIN_APPROX_SIMPLE)

        filtered = filter(lambda contour: cv2.contourArea(contour) > self.min_area, cnts)
        return map(lambda contour: cv2.boundingRect(contour), filtered)
