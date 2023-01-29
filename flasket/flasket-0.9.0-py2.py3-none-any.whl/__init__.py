import os

from .clients import client
from .flasket import Flasket
from .templates import template_global
from .wrappers import endpoint, require_http_same_origin

__all__ = [
    "Flasket",
]


rootpath = os.path.dirname(__file__)
