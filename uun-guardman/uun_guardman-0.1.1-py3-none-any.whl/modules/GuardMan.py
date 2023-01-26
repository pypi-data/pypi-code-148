import time
import argparse
import json
import json
import sys
import os
import datetime
from enum import Enum, IntEnum, auto
from typing import Dict, Any, AnyStr
from requests.exceptions import ConnectionError

import logging
logger = logging.getLogger(__name__)

from uun_iot import Module, on
from uun_iot_libledstrip import StripOverlayBundle, LedStrip, LedStripSegment
from uun_iot_libledstrip import Action, ActionType, hex2rgb
from uun_iot_libledstrip.devices import LedDev

# currently active app mode - SPECIAL state (error etc., see SpecialState) or BASIC (SegmentName) functionality
class Overlay(IntEnum):
    BASIC = auto()
    SPECIAL = auto()

# possible special states of the app (not basic functionality)
# right sides are the keys in config file
class SpecialState(Enum):
    ERROR = "error"

class SegmentName(Enum):
    PROGRESS = "progress"
    DELAY = "delay"
    CONNECTION = "connection"

class SegmentValue(Enum):
    pass

# possible values for the three segments
class Progress(SegmentValue):
    WAITING = "waiting"
    STARTED = "started"
    RUNNING = "running"
    RUNNING_WARNING = "runningWithWarning"
    RUNNING_ERROR = "runningWithError"
    COMPLETED = "completed"
    COMPLETED_WARNING = "completedWithWarning"
    COMPLETED_ERROR = "completedWithError"
    ERROR = "error"
    WARNING = "warning"

class Delay(SegmentValue):
    NO_DELAY = "noDelay"
    DELAYED_WARNING = "delayedWithWarning"
    DELAYED_ERROR = "delayedWithError"

class Connection(SegmentValue):
    CONNECTED = "connected"
    NO_CONNECTION = "noConnection"


class GuardMan(Module):
    _device: LedDev
    _segments: Dict[Any, LedStripSegment]
    # bundle a LedStrip for basic usage and another LedStrip for special state display
    _sbundle: StripOverlayBundle

    def __init__(self, config, get_uucmd, device=None):
        super().__init__(config=config)
        self._get_uucmd = get_uucmd

        if device is None:
            self._device = self._init_hw()
        elif isinstance(device, LedDev):
            self._device = device
        else:
            raise ValueError("device must be a LedDev device")

        # initialized segments from configuration entries "state, delay, connection"
        self._segments = self._init_basic_segments()
        strip = LedStrip(
                device=self._device,
                segments=self._segments,
            )

        # special state (errors) strip
        # initialized segments from configuration entry "special"
        sstrip = LedStrip(
                device=self._device,
                segments=self._init_special_segments(),
            )

        self._sbundle = StripOverlayBundle({
            Overlay.BASIC: strip,
            Overlay.SPECIAL: sstrip
        })

    def _init_hw(self) -> LedDev:
        """
        Initialize underlying LED strip. 
        Look at configuration `ledStrip/virtualMode` to determine whether to initialize a real HW LED strip or a virtual one.
        """
        n = self._c("ledStrip/pixels")
        if not self._c("ledStrip/virtualMode"):
            try:
                import board
                from uun_iot_libledstrip.devices import NeopixelDev
                pin_id = self._c("ledStrip/pin")
                pin = getattr(board, pin_id)
                device = NeopixelDev(
                    pin, n, brightness=0.1, auto_write=False
                )
                logger.debug(f"Initializized NeopixelDev with parameters: pin {pin}, {n} pixels.")
                return device
            except ImportError:
                logger.warning("Falling back to virtual LED strip, could not detect neccessary hw packages.")

        # fallback to virtual strip if not on rpi
        from uun_iot_libledstrip.devices import DebugLedDev
        device = DebugLedDev(n, colored=True)
        return device

    def _init_special_segments(self) -> Dict[int, LedStripSegment]:
        """ Special states have a single common segment with variable actions depending on state (see `self._set_special_state`). """
        return {
            0: LedStripSegment(
                device=self._device,
                leds = list(range(0, self._c("ledStrip/pixels"))),
                autoshow=False
            )
        }

    def _init_basic_segments(self) -> Dict[SegmentName, LedStripSegment]:
        """ All "progress, delay, connection" keys in configuration corresponds to one LED segment. """
        seg_map = {}
        for segment_name in [s.value for s in SegmentName]:
            centry = self._c(segment_name)
            min_led = centry["ledMinPosition"]
            max_led = centry["ledMaxPosition"]

            seg = LedStripSegment(
                    device=self._device,
                    leds=list(range(min_led, max_led + 1)),
                    autoshow=False,
                ) 
            seg_map[SegmentName(segment_name)] = seg
        return seg_map

    @on("tick")
    def on_tick(self):
        try:
            response = self._get_uucmd(self._c('progressCode'))
            if (response.status_code >= 200 and response.status_code < 300):
                response_date = response.headers['date']
                progress_data = json.loads(response.text)
                now = datetime.datetime.strptime(response_date, '%a, %d %b %Y %H:%M:%S %Z')
                self.evaluate_data(progress_data, now)
            else:
                self._set_basic_segment(SegmentName.CONNECTION, Connection.NO_CONNECTION)

        except ConnectionError:
            self._set_basic_segment(SegmentName.CONNECTION, Connection.NO_CONNECTION)
        except Exception as e:
            self._set_special_state(SpecialState.ERROR)
            raise e

    def evaluate_data(self, data, now):
        try:
            progress_state = Progress(data['state'])
        except ValueError:
            self._set_special_state(SpecialState.ERROR)
            raise ValueError(f"Invalid progress value encountered in received data: `{data['state']}`")

        # assign default values if delays (in seconds) are not specified
        delay_warning = data.get('delayWarning') or self._c('defaultDelays/warning')
        delay_error = data.get('delayError') or self._c('defaultDelays/error')

        # set delay state
        delay_state = Delay.NO_DELAY
        next_progress_ts = None
        if progress_state not in [Progress.COMPLETED, Progress.COMPLETED_WARNING, Progress.COMPLETED_ERROR]:
            timestamp_iso = data.get('estimatedNextProgressTs')
            if timestamp_iso is not None:
                next_progress_ts = datetime.datetime.strptime(timestamp_iso, '%Y-%m-%dT%H:%M:%S.%fZ')
                if now > next_progress_ts + datetime.timedelta(0, delay_error):
                    delay_state = Delay.DELAYED_ERROR
                elif now > next_progress_ts + datetime.timedelta(0, delay_warning):
                    delay_state = Delay.DELAYED_WARNING

        if delay_state != Delay.NO_DELAY:
            # zero out progress - remote process is delayed and is not reliable
            self._segments[SegmentName.PROGRESS].clear()
        else:
            self._set_basic_segment(SegmentName.PROGRESS, progress_state, show=False)

        self._set_basic_segment(SegmentName.CONNECTION, Connection.CONNECTED, show=False)
        self._set_basic_segment(SegmentName.DELAY, delay_state)

    def _set_special_state(self, state: SpecialState):
        """
        Set application special state.
        Display a SpecialState on the LED strip (currently whole strip, see self._init_state_segments),
          action for the strip/segments are taken from configuration. 
        """
        logger.info(f"Going into special app state {state}.")
        centry = self._c("special")[state.value]
        action = self._create_action_from_config(centry)

        self._sbundle.set_strip(Overlay.SPECIAL)
        self._sbundle.strip.activate(action)
        self._sbundle.strip.show()

    def _set_basic_segment(self, segment: SegmentName, action_name: SegmentValue, show=True):
        """ Make specified `segment` perform action specified by `action_name` in configuration. """
        try:
            action = self._create_action_from_config( 
                self._c(segment.value)[action_name.value]
            )
        except KeyError:
            raise ValueError(f"action_name {action_name} is not available in configuration under segment {segment}")

        self._sbundle.set_strip(Overlay.BASIC)
        self._segments[segment].activate(action)

        if show:
            self._sbundle.strip.show()

    def _create_action_from_config(self, centry: dict) -> Action:
        """ Create Action object from configuration dictionary with keys {action: ..., color: ..., interval: ...} """
        atype = ActionType.SOLID if centry["action"] == "solid" else ActionType.BLINK
        interval = centry["interval"]
        return Action(type=atype, color=hex2rgb(centry["color"]), period=interval)

