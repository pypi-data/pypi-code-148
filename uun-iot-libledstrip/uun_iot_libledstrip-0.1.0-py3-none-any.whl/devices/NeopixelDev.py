import neopixel
from .LedDev import LedDev

class NeopixelDev(neopixel.NeoPixel, LedDev):
    # already implements LedDev
    def __init__(self, *args, **kwargs):
        if len(args) >= 2:
            self._n = args[1]
        else:
            raise ValueError("Initialize this object in form of NeopixelDev(pin_id, number_of_leds, ...)")

        # auto_write is set on level of strips and segments
        kwargs["auto_write"] = False
        super(*args, **kwargs)

