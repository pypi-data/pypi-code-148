from .LedStrip import LedStripSegment, LedStrip
from .devices.LedDev import LedDev
from typing import List, Dict, Hashable
import math

class MeterStripSegment(LedStripSegment):
    """
    Visualize amount of some quantity. The Segment has to be constituted of succesive leds. 
    Based on dynamically varying amount of leds in LedStripSegment - number of leds depends on actual value of the measured quantity.
    Quantity is visualized from left to right -- left slots are allocated first.

    list `leds` and floats `value_min` and `value_max` are all inclusive -- boundary points are achieved
    """

    _possible_leds: List[int]
    _led_from: int
    _led_to: int
    _value_min: float
    _value_max: float

    def __init__(self,
            device: LedDev,
            autoshow: bool,
            leds: List[int], 
            *,
            value_min: float, value_max: float,
        ):

        self._possible_leds = leds
        super().__init__(device=device, autoshow=autoshow, leds=self._possible_leds)

        self._led_from = min(leds)

        # check that `leds` are formed from successive integers (the meter otherwise makes no sense)
        for i in range(0, self._n):
            if self._led_from + i != leds[i]:
                raise ValueError("List `leds` must be a list of successive integers, ie. no 'hole' is present in the list.")

        self._led_to = max(leds)
        self._value_min = value_min
        self._value_max = value_max

    def set_value(self, value: float):
        """
        Display a value on the segment.
        If the value is too large (larger or equal to val_to), set maximum number of leds on the segment.
        If the value is too low (strictly lower than val_from), set none leds.
        Otherwise there will always be some leds active.
        """

        if value < self._value_min:
            self._leds = []
            return

        if value > self._value_max:
            led_to = self._led_to
        else:
            percent = (value - self._value_min) / (self._value_max - self._value_min)
            led_to = min(self._led_from + math.floor(self._n * percent), self._led_to)

        self._leds = list(range(self._led_from, led_to + 1))

class MeterStrip(LedStrip):
    """
    Visualize amount of some quantity with tresholds indicating additional meaning. 
    Creates a strip from multiple MeterStripSegment(s).
    The segments do not have to span an interval. In the case there is a "hole" (value not in range of some segment)
      everything will still behave as expected (see definition of MeterStripSegment.set_value).
    """
    _value_min: float
    _value_max: float

    def __init__(self,
            device: LedDev,
            segments: Dict[Hashable, MeterStripSegment],
        ):
        
        # find global maximum and minimum values across all segments
        vmin = vmax = None
        for (i,s) in segments.items():
            vmin = s._value_min if vmin is None else min(vmin, s._value_min)
            vmax = s._value_max if vmax is None else max(vmax, s._value_max)

        self._value_max = vmax
        self._value_min = vmin

        super().__init__(device=device, segments=segments)

    def set_value(self, value, action=None):
        """
        Sets value of segments and invokes `action` on them, or stored action if action is None.
        Throws a ValueError if value is not in range supported by segments.
        """ 
        if not (self._value_min <= value <= self._value_max):
            raise ValueError("value is not between min and max")

        # search for segments to activate
        self.clear() # this will clear the whole strip (even inactive segments) as leds for clearing were initialized during __init__ in LedStrip
        for (key, s) in self._segments.items():
            s.set_value(value)
            s.activate(action)

