class HueStateChangeEvent:

    def __init__(self, sleep_time):
        """
        Represents data returned after a state change event in light status.

        :param sleep_time: amount of time (in seconds) that we should sleep after turning a light on.
        """
        self.sleep_time = sleep_time
