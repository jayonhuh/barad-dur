import datetime
from astral import *

now = datetime.datetime.now()


# Establish a location named oakland
oakland = Location()
oakland.name = 'Oakland'
oakland.region = 'west'
oakland.latitude = 37.778300
oakland.longitude = -122.181294
oakland.timezone = 'US/Pacific'
oakland.elevation = 35.6
oakland.sun()

def getSunrise():

    # create the sun object to get time value for sunrise and sunset
    sun = oakland.sun(date=datetime.date(now.year, now.month, now.day), local=True)

    sunrise_hour = int(sun['sunrise'].hour)
    sunrise_minute = int(sun['sunrise'].minute)

    return (sunrise_hour, sunrise_minute)


def getSunset():

    # create the sun object to get time value for sunrise and sunset
    sun = oakland.sun(date=datetime.date(now.year, now.month, now.day), local=True)

    sunset_hour = int(sun['sunset'].hour)
    sunset_minute = int(sun['sunset'].minute)

    return (sunset_hour, sunset_minute)

def main():

    # get sunruse and sunset
    sunrise_time = getSunrise()
    sunset_time = getSunset()

    print("hello")

    print(str(sunrise_time))
    print(str(sunset_time))

if __name__ == "__main__":
        main()

