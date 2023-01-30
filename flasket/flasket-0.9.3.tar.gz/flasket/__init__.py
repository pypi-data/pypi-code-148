import os

from .clients import client
from .decorators import endpoint
from .flasket import Flasket
from .templates import template_global

__all__ = [
    "Flasket",
]


rootpath = os.path.dirname(__file__)
