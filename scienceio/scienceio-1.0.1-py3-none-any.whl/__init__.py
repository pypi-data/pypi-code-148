import os

from .scienceio import HTTPError, ScienceIO, ScienceIOError  # noqa

__version__ = os.environ.get("SCIENCEIO_SDK_VERSION", "v0.0.1")
