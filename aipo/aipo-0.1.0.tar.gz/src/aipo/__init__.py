"""Aipo is a small and simple asyncio task/job queue."""

__version__ = "0.1.0"
__author__ = "Caique Reinhold"
__contact__ = "caiquereinhold@gmail.com"
__homepage__ = "https://github.com/CaiqueReinhold/aipo"
__keywords__ = "asyncio task job queue"
__docformat__ = "restructuredtext"

# -eof meta-

from .app import AipoApp as Aipo

__all__ = ("Aipo",)
