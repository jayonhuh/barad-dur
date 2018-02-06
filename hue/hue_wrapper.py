from phue import Bridge


class HueWrapper:

    def __init__(self, bridge_ip):
        """

        :param bridge_ip: ip address of the hue bridge
        """
        self.bridge = Bridge(bridge_ip)
        # first time we run, we have to press the physical button on the bridge device
        self.bridge.connect()

        lights = self.bridge.lights

        # Print light names
        print("found the following lights on bridge {}".format(bridge_ip))
        for l in lights:
            print(l.name)

    def is_group_on(self, group):
        """
        Checks whether the specified group is on.

        :param group:
        :return: True iff the specified group is on.
        """
        return self.bridge.get_group(group, "on")

    def turn_group_off(self, group):
        """
        Turns off the specified group.

        :param group:
        :return:
        """
        self.bridge.set_group(group, "on", False)

    def turn_group_on(self, group):
        """
        Turns on the specified group.

        :param group:
        :return:
        """
        self.bridge.set_group(group, "on", True)

    def set_light_group_brightness(self, group, brightness_pct):
        """
        Sets the brightness for the specified light group.

        Note that setting brightness to 0 will not turn off the light.

        :param group:
        :param brightness_pct:
        :return:
        """
        self.bridge.set_group(group, 'bri', self.brightness_from_pct(brightness_pct))

    def set_light_brightness(self, light, brightness_pct):
        """
        Sets the brightness for the specified light.

        Note that setting brightness to 0 will not turn off the light.

        :param light:
        :param brightness_pct:
        :return:
        """
        self.bridge.set_light(light, 'bri', self.brightness_from_pct(brightness_pct))

    @staticmethod
    def brightness_from_pct(brightness_pct):
        """
        Converts an integer representing percentage into a value acceptable for hue api

        :param brightness_pct:
        :return:
        """
        return int(float(brightness_pct) / 100 * 254)
