from .config import Settings

settings = Settings()

from . import _version
__version__ = _version.get_versions()['version']
