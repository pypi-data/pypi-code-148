import sys

if sys.version_info[:2] >= (3, 8):
    # TODO: Import directly (no need for conditional) when `python_requires = >= 3.8`
    from importlib.metadata import PackageNotFoundError, version  # pragma: no cover
else:
    from importlib_metadata import PackageNotFoundError, version  # pragma: no cover

raise RuntimeError(
    "pynvvideocodec does not contain any usable code at the moment. "
    "Please uninstall via `pip uninstall pynvvideocodec`")
