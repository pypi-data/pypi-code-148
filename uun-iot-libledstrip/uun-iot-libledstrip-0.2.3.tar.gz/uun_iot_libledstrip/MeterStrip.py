from typing import List, Dict, Hashable, Union, Optional, Callable, Tuple
import math

from .LedStrip import LedStripSegment, LedStrip, Action
from .devices.LedDev import LedDev

class MeterStripSegment(LedStripSegment):
    """ Visualize amount of some quantity on a LED strip (segment).

    This is done by linear interpolation
    between minimum and maximum possible value - maximum meaning all LEDs are lit.
    Based on dynamically varying amount of leds in LedStripSegment - number of leds
    depends on actual value of the measured quantity.
    Quantity is visualized from left to right -- left slots are allocated first.
    The Segment has to be comprised of succesive leds.

    list ``leds`` and floats ``value_min`` and ``value_max`` are all inclusive
    -- boundary points are achieved

    Args:
        device: underlying LedDev device
        autoshow: propagate every state change directly to hardware.
            Otherwise, a :meth:`~uun_iot_libledstrip.LedStrip.LedStrip.show` is needed
            to propagate changes explicitly.
        leds: a list of succesive integers (IDs of LEDs) forming the LED segment.
            These IDs are inclusive - maximum ID is achieved for maximal value.
        value_min: inclusive lower bound on value
        value_max: inclusive upper bound on value. ``value_max`` can be unbounded (None),
            indicating that the whole segment is fully active (all leds are activated)
            whenever value > value_min.
        hook_set_value: a function (float, List[int], Action) -> (List[int], Action) which,
            if specified, will be called at the end of :meth:`.set_value` as
            ``self._leds, self._action = hook_set_value(value, self._leds, self._action)``,
            ``value`` being currently set value, ``self._leds`` being a int list of current LED IDs
            and ``self._action`` being currently stored action.

    Raises:
        ValueError: when ``leds`` is not a list of succesive integers
        ValueError: when ``value_min`` is equal to ``value_max``

    Examples:
        Variable action based on set value:

            Example using the ``hook_set_value`` argument for changing stored action
            depending on the value. If it is too large (in this example, bigger than 100),
            store action with red color, otherwise store green color:

            .. code-block:: python

                def hook(value, leds, action):
                    if value > 100:
                        action = Action(ActionType.SOLID, color=(255,0,0))
                    else:
                        action = Action(ActionType.SOLID, color=(0,255,0))
                    return leds, action

                segment = MeterStripSegment(
                    device, autoshow=True, leds=[0,1,2,3,4],
                    value_min=5, value_max=200,
                    hook_set_value=hook
                )

                # definition of MeterStrip strip containing the segment
                strip = MeterStrip(device,[segment])

                strip.set_value(200)

                strip.set_value(50)

            >>> # the whole segment is lit red (255, 0, 0)
            >>> # some LEDs in the segment are lit green (0, 255, 0)
        """

    _possible_leds: List[int]
    _led_from: int
    _led_to: int
    _value_min: float
    _value_max: Optional[float]

    _hook_set_value: Optional[Callable[ [float, List[int], Action], Tuple[List[int], Action] ]]

    def __init__(self,
            device: LedDev,
            autoshow: bool,
            leds: List[int],
            *,
            value_min: float, value_max: Optional[float],
            hook_set_value: Optional[Callable[ [float, List[int], Action], Tuple[List[int], Action] ]]=None
        ):

        self._led_from = min(leds)
        self._led_to = max(leds)

        self._possible_leds = leds
        super().__init__(device=device, autoshow=autoshow, leds=self._possible_leds)

        # check that `leds` are formed from successive integers (the meter otherwise makes no sense)
        if leds != list(range(self._led_from, self._led_to + 1)):
            raise ValueError("List `leds` must be a list of successive integers, ie. no 'hole' is present in the list.")

        if value_min == value_max:
            raise ValueError("`value_min` cannot be same as `value_max`.")

        self._value_min = value_min
        self._value_max = value_max
        self._hook_set_value = hook_set_value

    def set_value(self, value: float):
        """Display the value on the segment.

        If the value is too large (larger or equal to ``value_max``, or ``value_max`` is ``None``),
        light ALL leds in the segment.
        If the value is too low (strictly lower than ``value_min``), light NO leds.
        Otherwise, there will be some active leds.

        If :func:`hook_set_value` was set during initialization, call the function at last
        with the newly modified values.
        See initialization for more information about :func:`hook_set_value`

        Args:
            value: value to be shown on the segment. Corresponding number of LEDs will
                be set active - the percentage of active leds will be the same
                as ``value/(value_max-value_min)``. LEDs are set active from lowest to highest IDs.
        """

        if value < self._value_min:
            self._leds = []
            if self._hook_set_value:
                self._leds, self._action = self._hook_set_value(value, self._leds, self._action)
            return

        # set number of leds
        # if `value_max` is unbounded (None) or `value` exceeds `value_max`, activate all leds
        # else interpolate linearly between `value_min` and `value_max`
        if self._value_max is None or value > self._value_max:
            led_to = self._led_to
        else:
            percent = (value - self._value_min) / (self._value_max - self._value_min)
            led_to = min(self._led_from + math.floor(self._n * percent), self._led_to)

        self._leds = list(range(self._led_from, led_to + 1))

        if self._hook_set_value:
            self._leds, self._action = self._hook_set_value(value, self._leds, self._action)

class MeterStrip(LedStrip):
    """Visualize amount of some quantity on a :class:`LedStrip`.

    Multiple segments of the strip can be specified to indicate additional meaning
    by visual distinction of each segment.

    The segments do not have to span an interval.
    In the case there is a "hole" (set value may not be in range of some segment)
    everything will still behave as expected, see definition of :meth:`MeterStripSegment.set_value`.
    """
    _value_min: float
    _value_max: Union[float, None]

    def __init__(self,
            device: LedDev,
            segments: Union[List[MeterStripSegment], Dict[Hashable, MeterStripSegment]]
        ):
        """
        Args:
            device: underlying LedDev device
            segments: dictionary of MeterStripSegments indexed by their IDs.
                If list of MeterStripSegments is passed instead,
                convert it to dictionary by using 0, 1, ..., n as keys.

        Raises:
            ValueError: when multiple segments have unbounded upper value limit (value_max = None)
            ValueError: when minimal and maximal values (``value_min`` and ``value_max``)
                taken across all segments in ``segments`` are the same
        """

        super().__init__(device=device, segments=segments)

        # find global maximum and minimum values across all segments
        count_max_none = 0
        vmin = vmax = None
        for (i,s) in self._segments.items():
            vmin = s._value_min if vmin is None else min(vmin, s._value_min)
            if s._value_max is None:
                count_max_none += 1
                continue
            vmax = s._value_max if vmax is None else max(vmax, s._value_max)

        if count_max_none > 1:
            raise ValueError("Multiple segments contain unbounded maximal value.")
        if count_max_none > 0:
            vmax = None

        if vmax == vmin:
            raise ValueError("Minimal and maximal value of Segments in ``segments`` must be different.")

        self._value_max = vmax
        self._value_min = vmin

    def set_value(self, value: float, action: Action=None):
        """Set displayed value on the meter and invoke action on activated LEDs.

        Sets value of segments and invokes ``action`` on them, or stored action if action is None.
        Value can be out of range of the segments.

        Args:
            value: value to be displayed, see :meth:`~MeterStrip.MeterStripSegment.set_value`
                for more information
            action: Action to invoke on activated LEDs in segments. If None, invoke
                stored action of the segment.
        """
        # search for segments to activate

        # this will clear the whole strip (even inactive segments)
        # as leds for clearing were initialized during __init__ in LedStrip
        self.clear() 
        for (key, s) in self._segments.items():
            s.set_value(value)
            s.activate(action)
