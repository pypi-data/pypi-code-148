from enum import Enum, auto
from dataclasses import dataclass
from typing import Optional

class ActionType(Enum):
    SOLID = auto()
    BLINK = auto()

@dataclass
class Action():
    type: ActionType
    color: tuple
    period: Optional[float]

def hex2rgb(value: str):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def rgb2hex(rgb: tuple):
    return '#{:02x}{:02x}{:02x}'.format( rgb[0], rgb[1] , rgb[2] )

from .LedStrip import LedStripSegment, LedStrip, StripOverlayBundle
from .MeterStrip import MeterStripSegment, MeterStrip

