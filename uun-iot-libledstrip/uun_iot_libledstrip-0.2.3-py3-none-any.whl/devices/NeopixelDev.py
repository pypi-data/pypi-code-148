import neopixel
from .LedDev import LedDev

class NeopixelDev(neopixel.NeoPixel, LedDev):
    """
    See `Adafruit NeoPixel <https://github.com/adafruit/Adafruit_CircuitPython_NeoPixel>`_. ``autowrite`` is always ``False``, set it instead at level of :class:`LedStrip`
    """
    # already implements LedDev
    def __init__(self, *args, **kwargs):
        if len(args) >= 2:
            self._n = args[1]
        else:
            raise ValueError("Initialize this object in form of NeopixelDev(pin_id, number_of_pixels, ...)")

        # auto_write is set on level of strips and segments
        kwargs["auto_write"] = False
        super().__init__(*args, **kwargs)

