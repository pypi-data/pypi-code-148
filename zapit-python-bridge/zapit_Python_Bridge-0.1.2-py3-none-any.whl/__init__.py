from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("zapit-Python-Bridge")
except PackageNotFoundError:
    # package is not installed
    pass


# TODO -- something like this so we can import more easily
# from . import bridge
