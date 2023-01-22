import datetime
import numpy as np
import platform
import re

# Platform identification constants.
UNKNOWN          = 0
RASPBERRY_PI     = 1
BEAGLEBONE_BLACK = 2


class DHT():
    """ Wrapper for DHT sensor class that supports emulation to enable testing on other
    (non-Raspberry Pi) platforms
    """
    def __init__(self, emulate=False):
        self.emulate = emulate
        if not self.emulate:
            if platform_detect() != UNKNOWN:
                import Adafruit_DHT
            else:
                print('Not a Raspberry Pi. Reverting to DHT Emulation Mode')
                self.emulate = True
        else:
            print('DHT Emulation Mode')

    def read(self, sensor, pin, **kwargs):
        if not self.emulate:
            Adafruit_DHT.read(self, sensor, pin, **kwargs)
        else:
            dt = datetime.datetime.now()
            sin_day = np.sin(((dt.hour * 60 + dt.minute) * 60 + dt.second) / 60.0 / 60.0 / 24.0)
            temperature = 20.0 - sin_day * 10.0 + np.random.normal(0.0, 0.5)
            humidity = 50.0 + sin_day * 10.0 + np.random.normal(0.0, 0.5)
            return (humidity, temperature)

    def read_retry(self, sensor, pin, retries=15, **kwargs):
        if not self.emulate:
            Adafruit_DHT.read_retry(sensor, pin, **kwargs)
        else:
            dt = datetime.datetime.now()
            sin_day = np.sin(((dt.hour * 60 + dt.minute) * 60 + dt.second) / 60.0 / 60.0 / 24.0)
            temperature = 20.0 - sin_day * 10.0 + np.random.normal(0.0, 0.5)
            humidity = 50.0 + sin_day * 10.0 + np.random.normal(0.0, 0.5)
            return (humidity, temperature)


def platform_detect():
    """Detect if running on the Raspberry Pi or Beaglebone Black and return the
    platform type.  Will return RASPBERRY_PI, BEAGLEBONE_BLACK, or UNKNOWN."""
    # Handle Raspberry Pi
    pi = pi_version()
    if pi is not None:
        return RASPBERRY_PI

    # Handle Beaglebone Black
    # TODO: Check the Beaglebone Black /proc/cpuinfo value instead of reading
    # the platform.
    plat = platform.platform()
    if plat.lower().find('armv7l-with-debian') > -1:
        return BEAGLEBONE_BLACK
    elif plat.lower().find('armv7l-with-ubuntu') > -1:
        return BEAGLEBONE_BLACK
    elif plat.lower().find('armv7l-with-glibc2.4') > -1:
        return BEAGLEBONE_BLACK
    elif plat.lower().find('armv7l-with-arch') > -1:
        return BEAGLEBONE_BLACK

    # Couldn't figure out the platform, just return unknown.
    return UNKNOWN

def pi_version():
    """Detect the version of the Raspberry Pi.  Returns either 1, 2, 3 or
    None depending on if it's a Raspberry Pi 1 (model A, B, A+, B+),
    Raspberry Pi 2 (model B+), Raspberry Pi 3,Raspberry Pi 3 (model B+) or not a Raspberry Pi.
    """
    # Check /proc/cpuinfo for the Hardware field value.
    # 2708 is pi 1
    # 2709 is pi 2
    # 2835 is pi 3
    # 2837 is pi 3b+
    # Anything else is not a pi.
    with open('/proc/cpuinfo', 'r') as infile:
        cpuinfo = infile.read()
    # Match a line like 'Hardware   : BCM2709'
    match = re.search('^Hardware\s+:\s+(\w+)$', cpuinfo,
                      flags=re.MULTILINE | re.IGNORECASE)
    if not match:
        # Couldn't find the hardware, assume it isn't a pi.
        return None
    if match.group(1) == 'BCM2708':
        # Pi 1
        return 1
    elif match.group(1) == 'BCM2709':
        # Pi 2
        return 2
    elif match.group(1) == 'BCM2835':
        # Pi 3
        return 3
    elif match.group(1) == 'BCM2837':
        # Pi 3b+
        return 3
    else:
        # Something else, not a pi.
        return None
