from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional

class ActionType(Enum):
    #: Static color
    SOLID = auto()
    #: Blinking
    BLINK = auto()

@dataclass
class Action():
    """Object representing possible visualization actions on :class:`LedStrip`.

    Light LED up with given color or blink with given color and specified period.
    """
    type: ActionType
    color: tuple
    period: Optional[float]=None

def hex2rgb(value: str) -> tuple:
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def rgb2hex(rgb: tuple) -> str:
    return '#{:02x}{:02x}{:02x}'.format( rgb[0], rgb[1] , rgb[2] )

from .LedStrip import LedStripSegment, LedStrip, StripOverlayBundle
from .MeterStrip import MeterStripSegment, MeterStrip

