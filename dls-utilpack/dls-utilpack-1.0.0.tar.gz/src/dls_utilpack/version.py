"""
The version of the package can be returned as a single string or a dict.

When a string, it comes from the package __version__.
When a dict, it also has __version__,
as well as versions of other depdency packages.
"""

from importlib.metadata import version as importlib_metadata_version
from typing import Optional

import dls_logformatter.version

from dls_utilpack import __version__


# ----------------------------------------------------------
def version() -> str:
    """
    Version of the dls_utilpack package as a string.
    """

    return __version__


# ----------------------------------------------------------
def meta(given_meta: Optional[dict] = None) -> dict:
    """
    Returns version information from the dls_utilpack package
    and its dependencies as a dict.
    Adds version information to a given meta dict if it was provided.
    """

    meta = {}
    meta["dls_utilpack"] = version()
    meta.update(dls_logformatter.version.meta())

    packages = ["ruamel.yaml"]
    for package in packages:
        meta[package] = importlib_metadata_version(package)

    if given_meta is not None:
        given_meta.update(meta)
    else:
        given_meta = meta
    return given_meta
