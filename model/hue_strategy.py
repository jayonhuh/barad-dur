class HueStrategy:

    def __init__(self, hue_group, brightness, sleep_when_on):
        """
        Groups together behavior for interacting with hue lights.

        :param hue_group: identifier of the group we are controlling
        :param brightness: lambda returning the brightness of the light to set when turning on.
                           hue expresses this as a value in the range [0, 254],
                           but we express this here as percentage, ie a value in the range [0, 100]
        :param sleep_when_on: lambda returning the time to sleep after we have just turned on a light
        """
        self.hue_group = hue_group
        self.brightness = brightness
        self.sleep_when_on = sleep_when_on
