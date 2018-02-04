from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

"""
Captures and displays a single image.
"""

# we want to use rawcapture here, direct access to the camera stream
camera = PiCamera()
rawCapture = PiRGBArray(camera)

# let the sensor warm up
time.sleep(0.1)

camera.capture(rawCapture, format="bgr")
image = rawCapture.array

cv2.imshow("test image", image)
cv2.waitKey(0)
