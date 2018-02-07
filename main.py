
# loop over the video frames

# check for motion
# if the light is off:

#   if there is motion, run the person detector

#       if there is a person
#           turn on the lights.
#           the brightness should be a function of the time of day, including sunset/sunrise time
#           sleep for a certain amount of time. this should also be a function of the time of day

# if the light is on:
#   if there is motion, run the person detector:
#       if there is a person, keep the lights on and sleep
#       otherwise, turn the lights off and don't sleep
#


from hue.hue_wrapper import HueWrapper
from optics.human_detector import HumanDetector
from optics.motion_detector import MotionDetector
from model.hue_strategy import HueStrategy
from model.hue_state_change import HueStateChangeEvent
from util.graceful_killer import GracefulKiller
from picamera.array import PiRGBArray
from picamera import PiCamera
from threading import Event

import cv2
import datetime
import pytz
import sys
import time

def get_camera():
    """
    Connects to the camera

    :return: a handle to the camera and its capture feed
    """
    resolution = (640, 480)
    camera = PiCamera()
    camera.resolution = resolution
    camera.framerate = 2
    camera.contrast = 100
    # camera.brightness = 100
    camera.iso = 800
    raw_capture = PiRGBArray(camera, size=resolution)
    # warmup the sensor array
    time.sleep(0.1)
    return (camera, raw_capture)


def scan(camera, capture, hue, strategy):
    """
    Scans the video stream for motion and humans.

    :param camera:
    :param capture:
    :param hue:
    :param strategy:
    :return:
    """
    human_detector = HumanDetector()
    motion_detector = MotionDetector(min_area=300)
    human_threshold = 0.2

    initial_frame = None
    print("scanning video stream...")
    for frame in camera.capture_continuous(capture, format="bgr", use_video_port=True):
        # make sure we initialize the first frame TODO look for a nicer to consume the first frame
        if initial_frame is None:
            initial_frame = frame.array
            capture.truncate(0)
            continue

        frame = frame.array
        motion_rects = motion_detector.detect(initial_frame, frame)
        if len(list(motion_rects)) > 0:
            print("found motion {}".format(list(motion_rects)))

            # the lights are already on and we found motion. leave them on and go back to sleep.
            # its too slow to rely on the person detector here
            if hue.is_group_on(strategy.hue_group):
                break

            (human_rects, human_weights) = human_detector.detect(frame)
            # filter on a small threshold to avoid false positives
            filtered_weights = filter(lambda w: w > human_threshold, human_weights)
            # TODO we should also check that the rects are overlapping
            if len(list(filtered_weights)) > 0:
                print \
                    ("found humans above threshold {}, turning on {} lights".format(human_threshold, strategy.hue_group))
                hue.set_light_group_brightness(strategy.hue_group, strategy.brightness())
                hue.turn_group_on(strategy.hue_group)
                break
            # just print that we are likely avoiding a false positive
            elif len(human_rects) > 0:
                print("found humans below threshold {} (likely false positive)".format(human_threshold))

        elif hue.is_group_on(strategy.hue_group):
            print("turning off {} lights".format(strategy.hue_group))
            hue.turn_group_off(strategy.hue_group)

        initial_frame = frame
        # we need to truncate the buffer before the next iteration
        capture.truncate(0)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            sys.exit(1)

    return HueStateChangeEvent(strategy.sleep_when_on)

def get_brightness():
    """
    TODO this should lookup sunrise and sunset time
    TODO this should return a tuple and be combined with get_brightness()
    :return: the brightness we should set the lights to based on time of day.
    """
    hour = datetime.datetime.now(pytz.timezone('US/Pacific')).hour
    # late night
    if hour <= 3:
        return 20
    # late night
    elif hour <= 8:
        return 20
    # early morning
    elif hour <= 10:
        return 100
    # during work
    elif hour <= 17:
        return 50
    else:
        return 100


def get_sleep_time():
    """
    TODO this should lookup sunrise and sunset time
    TODO this should return a tuple and be combined with get_brightness()
    :return: the amount of time (in seconds) that we should sleep for after turning the lights on.
    """
    hour = datetime.datetime.now(pytz.timezone('US/Pacific')).hour
    # late night
    if hour <= 1:
        return 360
    # late night
    elif hour <= 8:
        return 120
    # early morning
    elif hour <= 10:
        return 180
    # during work
    elif hour <= 17:
        return 45
    # evening
    elif hour <= 22:
        return 500
    else:
        return 360

def quit(signo, _frame):
    print("Interrupted by %d, shutting down" % signo)
    exit.set()



def main():
    """
    Main script loop.

    Creates a hue wrapper and monitors the video stream.
    :return:
    """
    hue = HueWrapper("10.0.1.35")

    # create a strategy
    strategy = HueStrategy("Kitchen", lambda: get_brightness(), lambda: get_sleep_time())

    # handle sigkill signals when we get restarted
    exit_handler = Event()

    (camera, capture, result) = None, None, None

    while not exit_handler.is_set():
        # create a camera
        (camera, capture) = get_camera()
        # scan the video stream
        result = scan(camera, capture, hue, strategy)
        print("sleeping for {}s".format(result.sleep_time()))
        exit_handler.wait(result.sleep_time())

    if camera is not None:
        camera.close()

    if capture is not None:
        capture.close()

if __name__ == "__main__":

    import signal

    for sig in ('TERM', 'KILL', 'HUP', 'INT'):
        signal.signal(getattr(signal, 'SIG' + sig), quit)

    main()
