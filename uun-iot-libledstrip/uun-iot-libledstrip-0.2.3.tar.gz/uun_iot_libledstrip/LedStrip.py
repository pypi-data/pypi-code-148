import threading
import logging
from typing import Optional, Dict, List, Hashable, Any, Union, Callable

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
    Create an autonomous segment in a LED strip.

    Args:
        device: an underlying LedDev instance
        leds: a list with pixel IDs. A segment will be created from these IDs. These does not have to be consecutive IDs.
        autoshow: invoke :meth:`.show` after every :meth:`.set_color` call
            if set to ``False``, blinking will still trigger :meth:`.show` (as expected)
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
        self._leds = leds
        self._autoshow = autoshow
        self._device = device
        self._blink_stopev = threading.Event()
        self._t = None
        self._n = len(leds)
        self._action = None

    @property
    def leds(self):
        """ Read-only list of available leds. """
        return self._leds

    def show(self):
        """ Refreshes WHOLE hardware strip, not only this segment. """
        self._device.show()

    def store_action(self, action: Action):
        """Store action.

        Store action so that one does not have to specify colors (or blinking) every time. Invoke stored ``action`` with :meth:`.activate`.

        Args:
            action: :class:`~uun_iot_libledstrip.Action` object to be stored
        """
        self._action = action

    def activate(self, action: Optional[Action]=None):
        """Invoke action.

        Args:
            action: Action instance. If ``None``, invoke stored action. See :meth:`.store_action`.

        Raises:
            ValueError: ``action`` is ``None`` and no action was stored earlier
        """
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

        Args:
            col: RGB tuple
            clear_blink: clear any blinking present before setting colors, defaults to ``True``
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
        """Clear segment.

        Set color of the segment to ``(0,0,0)``.

        Args:
            clear_blink: pass the same value to function :meth"`.set_color`, see documentation there. Defaults to ``True``.
        """
        self.set_color((0,0,0), clear_blink)

    def clear_blink(self):
        """Stop blinking."""
        if self._t:
            self._blink_stopev.set()
            # block until thread is finished
            self._t.join()
            self._t = None
            self._blink_stopev.clear()

    def set_color_blink(self, col: tuple, period: float, runonstart: bool=True):
        """Specify blinking.

        Blink the specified color with period (s). 
        Whole strip is :meth:`.show`-n after each blink (as each segment can have different period, there is no other way to do this without checking for same period of all segments).

        Args:
            col: RGB tuple color to blink with
            period: period of blinking (seconds)
            runonstart: if True, begin the cycle with setting color. Otherwise, wait first for ``period`` s. Defaults to True
        """

        if self._leds == []:
            return

        self.clear_blink()

        def c_show():
            """ Conditionally refresh the strip. Ensure exactly one :meth:`.show` refresh call regardless of self._autoshow settings. """
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
    """ A collection of LedStripSegments forming a led strip.

    Args:
        device: an underlying LedDev instance
        segments: dictionary with values being LedStripSegment objects.
            Specifies segments of the led strip based on dictionary keys.
            If list of LedStripSegment(s) is given instead, the segments in the list
            will be addressable by list indices (0, 1, .... n).

    Raises:
        TypeError: when segments is nor list nor dictionary
    """
    _n: int
    _segments: Dict[Hashable, LedStripSegment]
    _device: LedDev
    _leds: List[int]

    def __init__(self,
            device: LedDev,
            segments: Union[List[LedStripSegment], Dict[Hashable, LedStripSegment]],
        ):

        if isinstance(segments, list):
            segments = dict(zip(range(len(segments)), segments))

        if not isinstance(segments, dict):
            raise TypeError("segments must be a Dict[Hashable, LedStripSegment]")

        self._segments = segments
        self._device = device

        self._leds = []

        for (i, s) in segments.items():
            self._leds.extend(s.leds)
        self._n = len(self._leds)

    def _action_on_segments(self, fn: Callable[[LedStripSegment], None], segment_id: Hashable=None):
        """
        Apply function ``fn`` to segment indexed by ``segment_id``.

        Args:
            fn: function
            segment_id: segment index. If ``None``, iterate over all segments.

        Raises:
            ValueError: if segment with ``segment_id`` does not exist
        """
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
        Activate an action for segment identified by ``segment_id``. 

        Args:
            action: Action to be applied to segment using ``segment.activate(action)``. If ``None``, activate segments stored action. Defaults to ``None``.
            segment_id: segment's key in segment dictionary. If ``None``, apply to all segments. Defaults to ``None``.
        """

        self._action_on_segments(lambda s: s.activate(action), segment_id)

    def set_color(self, col: tuple, segment_id=None):
        """Set color of a segment.
        
        Args:
            segment_id: segment's key in segment dictionary. If ``None``, set color of all segments.
            col: RGB tuple
        """
        self._action_on_segments(lambda s: s.set_color(col), segment_id)

    def set_color_blink(self, col, period, segment_id=None):
        """Set blinking of a segment.
        
        Args:
            col: RGB color tuple
            period: period of blinking in seconds
            segment_id: segment's key in segment dictionary. If None, set color of all segments.
        """
        self._action_on_segments(lambda s: s.set_color_blink(col, period), segment_id)

    def show(self):
        self._device.show()

    def clear_leds(self, leds: List[int]):
        """ Clear LEDs. This will not stop blinking nor .show() the strip.

        Set color of specified LEDs to (0,0,0).

        Args:
            leds: list of LEDs to be cleared
        """
        for l in leds:
            self._device[l] = (0,0,0)

    def clear_strip(self):
        """
        Clear LED strip in one go. Prevent sending :meth`:.show` multiple times from each segment if ``autoshow=True`` for some segments.
        This will not .show() the strip.
        """
        self._action_on_segments(lambda s: s.clear_blink())
        self.clear_leds(self._leds)
        # self._device.show()

    def clear(self, segment_id: Hashable=None):
        """ Clear a segment, this includes clearing blinking. Set ``segment_id`` to ``None`` (default) clear whole strip. """
        if segment_id is None:
            self.clear_strip()
        else:
            self._action_on_segments(lambda s: s.clear(), segment_id)

#    def __del__(self):
#        logger.debug(f"{self.__class__.__name__} cleared.")
#        self.clear_strip()
#        self.show()

class StripOverlayBundle:
    """A class to pack different :class:`LedStrip` instances and set a single currently active strip among them.
    
    This can be used to add multiple different exclusive display modes (meaning exactly one of them will be active at a time) to the physical strip.
    Main reason for using this class is only logical with the advantage being confidence,
    that the various bundled strips will accidentally not be active at the same time.

    Example:
        The :class:`StripOverlayBundle` will act as a meter (:class:`~uun_iot_libledstrip.MeterStrip.MeterStrip`) in normal circumstances but will be replaced by 
        an `error` :class:`LedStrip` in case of an error:

        .. code-block:: python
    
            error_action = Action(type=ActionType.BLINK, color=(255,0,0), period=.2)
            class State(Enum):
                NORMAL=1,
                ERROR=2

            overlays = {
                State.NORMAL: MeterStrip(leddevice, segments),
                State.ERROR: LedStrip(leddevice, segments2)
            }
            overlay = StripOverlayBundle(overlays)

            if status=="OK":
                overlay.set_strip(State.NORMAL)
                overlay.strip.set_value(25)
            else:
                overlay.set_strip(State.ERROR)
                overlay.strip.activate(error_action)

            overlay.strip.show()

    Args:
        strips: dictionary with values being LedStrip objects.
            Specifies overlays of the real physical strip based on dictionary keys.
            If list of LedStrip(s) is given instead, the strips in the list
            will be addressable by list indices ``(0, 1, ..., n)``.

    Raises:
        TypeError: when ``segments`` is nor a list nor a dictionary
    """
    #: currently set strip
    strip: LedStrip
    _overlays: Dict[Hashable, LedStrip]

    def __init__(self, strips: Union[List[LedStrip], Dict[Hashable, LedStrip]]):

        if isinstance(strips, list):
            segments = dict(zip(range(len(strips)), strips))

        if not isinstance(strips, dict):
            raise TypeError("strips must be a Dict[Hashable, LedStripSegment]")
        self.strip = None
        self._overlays = strips

    def set_strip(self, index: Hashable):
        """Display/set active overlay given by ``index``.

        Clear currently active strip (if set and is different from a new one) and replace :attr:`.strip` with a strip on position ``index``.
        This does not affect the underlying :class:`LedDev` device immedieately (ie. ``self.strip.show()`` is needed to propagate changes from the new strip to underlying LedDev device).

        Args:
            index: index of strip to be set as visible
        """
        if self._overlays[index] == self.strip:
            return

        if self.strip is not None:
            self.strip.clear()

        logger.debug(f"Setting strip overlay to {index!r}.")
        self.strip = self._overlays[index]

