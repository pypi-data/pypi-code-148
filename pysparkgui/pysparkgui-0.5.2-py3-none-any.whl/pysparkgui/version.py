# Copyright (c) Databricks Inc.
# Distributed under the terms of the DB License (see https://databricks.com/db-license-source
# for more information).

import requests
import packaging.version
import ipywidgets as widgets
import pysparkgui.config as _config

from pysparkgui.helper.utils import notification
from pysparkgui import __version__

PYPI_pysparkgui_URL = "https://pypi.org/pypi/pysparkgui/json"

UPDATE_pysparkgui_VERSION_URL = "https://docs.pysparkgui.8080labs.com/documentation/how-tos/installation-and-setup/update-to-a-new-version-of-pysparkgui"

pysparkgui_RELEASE_HISTORY_URL = (
    "https://docs.pysparkgui.8080labs.com/etc/release-history"
)

NEW_VERSION_MESSAGE_DATABRICKS = f"""
    A new pysparkgui version is available. Run <code>%pip install pysparkgui -U</code> in your notebook to upgrade.
"""


def _version_str_to_obj(version_str):
    """Convert the release version string into a version object."""
    return packaging.version.Version(version_str)


def _get_latest_pysparkgui_version(timeout=None):
    """Gets the latest pysparkgui version from pypi.org

    :param timeout: float or None. The timeout in seconds

    :return: The latest pysparkgui version as a version object
    """
    result = requests.get(PYPI_pysparkgui_URL, timeout=timeout)
    try:
        version_str = result.json()["info"]["version"]
    except Exception as exception:
        raise RuntimeError("Got unexpected response from PyPI", exception)
    return _version_str_to_obj(version_str)


def _get_installed_pysparkgui_version():
    return _version_str_to_obj(__version__)


def _should_show_new_version_notification():
    """Return True if we have a newer version and haven't informed the user yet."""
    if not _config.SHOW_NEW_VERSION_NOTIFICATION:
        # We only show the notification once per session
        return False

    try:
        installed_version = _get_installed_pysparkgui_version()
        latest_version = _get_latest_pysparkgui_version(timeout=1)
    except Exception:
        return False

    return latest_version > installed_version


def maybe_show_new_version_notification():
    from pysparkgui._authorization import auth

    if _should_show_new_version_notification() and auth.is_databricks():
        return notification(NEW_VERSION_MESSAGE_DATABRICKS, type="warning")
    else:
        return widgets.HTML()
