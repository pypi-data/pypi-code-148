import threading
import logging
from typing import Optional, Dict, List, Hashable, Any

from abc import ABC, abstractmethod
from .devices.LedDev import LedDev
from . import Action, ActionType


logger = logging.getLogger(__name__)


class LedStripInterface(ABC):

    @abstractmethod
    def show(self):
        pass

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def activate(self, *args, **kwargs):
        pass

    @abstractmethod
    def set_color(self, *args, **kwargs):
        pass

    @abstractmethod
    def set_color_blink(self, *args, **kwargs):
        pass

class LedStripSegment(LedStripInterface):
    """
    Create an autonomous segment of a LED strip.
    """
    _leds: list
    _autoshow: bool
    _device: LedDev
    _blink_stopev: threading.Event # signal blinking stop
    _t: Optional[threading.Thread]
    _n: int
    _action: Optional[Action]

    def __init__(self,
            device: LedDev,
            leds: List[int],
            autoshow: bool
        ):
        """
        device: an underlying LedDev instance
        leds: a list with pixel IDs. A segment will be created from these IDs. These does not have to be consecutive IDs.
        autoshow: (bool) invoke `self.show()` after every `.set_color()` call
            if set to False, blinking will still trigger show (as is to be expected)
        """
        self._leds = leds
        self._autoshow = autoshow
        self._device = device
        self._blink_stopev = threading.Event()
        self._t = None
        self._n = len(leds)

    @property
    def leds(self):
        """ Read-only list of available leds. """
        return self._leds

    def show(self):
        """ Refreshes WHOLE hardware strip, not only this segment. """
        self._device.show()

    def store_action(self, action: Action):
        """ Store action so that one does not have to specify colors (or blinking) every time. Invoke stored action with .activate(). """
        self._action = action

    def activate(self, action: Optional[Action]=None):
        """ Invoke action. If action is None, stored action will be invoked, if present. See store_action. """
        if action is None:
            action = self._action

        if action is None:
            raise ValueError("define action first via store_action")

        if action.type == ActionType.SOLID:
            self.set_color(action.color)
        elif action.type == ActionType.BLINK:
            self.set_color_blink(action.color, action.period)

    def set_color(self, col: tuple, clear_blink: bool=True):
        """ 
        Set color of whole strip and display immediately.
        col: color in RGB tuple
        clear_blink: default True, clear any blinking present before setting colors
        """

        if clear_blink:
            self.clear_blink()

        # sets all available leds in segment -- no need to clear
        for i in self._leds:
            self._device[i] = col

        if self._autoshow and self._leds != []:
            # unncecessary show otherwise
            self.show()

    def clear(self, clear_blink: bool=True):
        """
        Set color of the segment to (0,0,0).
        stop_blink: defaults to True, pass the same value to function `.set_color`, see documentation there
        """
        self.set_color((0,0,0), clear_blink)

    def clear_blink(self):
        if self._t:
            self._blink_stopev.set()
            # block until thread is finished
            self._t.join()
            self._t = None
            self._blink_stopev.clear()

    def set_color_blink(self, col: tuple, period: float, runonstart: bool=True):
        """
        Blink the specified color with period (s). 
        Whole strip is `.show`n after each blink (as each segment can have different period, there is no other way to do this without checking for same period of all segments).
        col: color to blink with, tuple with three elements
        period: period of blinking
        runonstart: default True, if runonstart is True, set color first. Otherwise, wait first.
        """

        self.clear_blink()

        def c_show():
            """ Conditionally refresh the strip. Ensure exactly one `.show` refresh call regardless of self._autoshow settings. """
            if not self._autoshow:
                self._device.show()

        def _repeat():
            if runonstart:
                self.clear(clear_blink=False)
                self.set_color(col, clear_blink=False)
                c_show()

            # switch periodically between empty segment and specified color
            while not self._blink_stopev.is_set():
                self._blink_stopev.wait(period)
                self.clear(clear_blink=False)
                c_show()

                self._blink_stopev.wait(period)
                self.set_color(col, clear_blink=False)
                c_show()

        # daemon -- program can exit even when there are daemon threads running
        self._t = threading.Thread(target=_repeat, daemon=True)
        self._t.start()

class LedStrip(LedStripInterface):
    """ A collection of LedStripSegments forming a led strip. """
    _n: int
    _segments: Dict[Hashable, LedStripSegment]
    _device: LedDev
    _leds: List[int]

    def __init__(self,
            device: LedDev,
            segments: Dict[Hashable, LedStripSegment],
        ):

        if not isinstance(segments, dict):
            raise ValueError("segments must be a Dict[Hashable, LedStripSegment]")

        self._segments = segments
        self._device = device

        self._leds = []

        for (i, s) in segments.items():
            self._leds.extend(s.leds)
        self._n = len(self._leds)

    def _action_on_segments(self, fn, segment_id=None):
        """ Apply action `fn` to segment_id. If segment_id is None, apply to all segments. """
        if segment_id is None:
            for (sid, s) in self._segments.items():
                fn(s)
            return

        try:
            s = self._segments[segment_id]
        except KeyError:
            raise ValueError("Segment does not exist.")

        fn(s)

    def activate(self, action: Action=None, segment_id=None):
        """
        Activate an action on segment_id segment. 
        action: if None (default), apply segment's stored action. Otherwise apply `action`.
        segment_id: segment's key in segment dictionary
        """

        self._action_on_segments(lambda s: s.activate(action), segment_id)

    def set_color(self, col: tuple, segment_id=None):
        """ Set color of a segment. Set segment_id to None (default) to set all segments. """
        self._action_on_segments(lambda s: s.set_color(col), segment_id)

    def set_color_blink(self, col, period, segment_id=None):
        """ Blink the specified color with period (s).. Set segment_id to None (default) to set all segments. """
        self._action_on_segments(lambda s: s.set_color_blink(col, period), segment_id)

    def show(self):
        self._device.show()

    def clear_leds(self, leds: List[int]):
        """ Clear only these LEDs. This will not .show() the strip. """
        for l in leds:
            self._device[l] = (0,0,0)

    def clear_strip(self):
        """
        Clear LED strip in one go. Prevent sending `show` multiple times from each segment if autoshow=True for some segments.
        This will not .show() the strip.
        """
        self._action_on_segments(lambda s: s.clear_blink())
        self.clear_leds(self._leds)
        # self._device.show()

    def clear(self, segment_id=None):
        """ Clear a segment. Set segment_id to None (default) clear whole strip. """
        if segment_id is None:
            self.clear_strip()
        else:
            self._action_on_segments(lambda s: s.clear(), segment_id)

#    def __del__(self):
#        logger.debug(f"{self.__class__.__name__} cleared.")
#        self.clear_strip()
#        self.show()

class StripOverlayBundle:
    """
    A class to pack different LedStrip instances and set a single currently active strip among them.
    This can be used to add multiple different display modes to the physical strip.
    Eg. the strip will act as a meter (MeterStrip) in normal circumstances but will be replaced by 
      a (full-lit) normal LedStrip in case of an error.
    """
    strip: LedStrip
    _overlays: Dict[Hashable, LedStrip]

    def __init__(self, strips: Dict[Hashable, LedStrip]):
        self.strip = None
        self._overlays = strips

    def set_strip(self, index: Hashable):
        """ 
        Clear currently active strip (if set and is different from a new one) and replace `self.strip` with a strip on position `index`.
        This does not affect the undelying LedDev device immedieately.
        """
        new = self._overlays[index]

        if self.strip == new:
            return
        if self.strip is not None:
            self.strip.clear()

        logger.debug(f"Setting strip overlay to {index!r}.")
        self.strip = self._overlays[index]

