import os
import platform
import re
from importlib.metadata import version
from pathlib import Path


def validate_mac(addr: str) -> bool:
    """
    Mac address validation regex

    Args:
        addr: the mac address (with colons)
    Returns:
        True if this is a valid mac address
    """
    return bool(
        re.match("^([0-9a-fA-F][0-9a-fA-F]:){5}([0-9a-fA-F][0-9a-fA-F])$", addr)
    )


def validate_uuid(u: str) -> bool:
    """
    UUID validation regex

    Args:
        addr: the uuid
    Returns:
        True if this is a valid UUID
    """
    return bool(
        re.match(
            "[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}",
            u,
        )
    )


def get_appdata_dir() -> Path:
    """
    Get the path to a bluerpc appdata folder

    Returns:
        a path object to this folder
    """
    if platform.system() == "Windows":
        p = os.getenv("LOCALAPPDATA")
    elif platform.system() == "Darwin":
        p = "~/Library/Application Support"
    else:
        p = os.getenv("XDG_DATA_HOME", "~/.local/share")

    return Path(p).expanduser().joinpath("bluerpc")


def get_version() -> str:
    """
    Helper to get the current version of our package

    Returns:
        the version if found, else 0.0.0
    """
    try:
        return version("bluerpc")
    except Exception:
        return "0.0.0"
