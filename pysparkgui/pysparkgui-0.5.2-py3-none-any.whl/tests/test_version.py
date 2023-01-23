import requests
import ipywidgets as widgets

import pysparkgui
from pysparkgui.version import (
    _version_str_to_obj,
    _get_latest_pysparkgui_version,
    _should_show_new_version_notification,
)

from packaging.version import Version


def test_version_str_to_obj():
    assert _version_str_to_obj("1.1.0") == Version("1.1.0")


def test_get_latest_pysparkgui_version(monkeypatch):
    class MockResponse:
        def json(self):
            return {"info": {"version": "1.10.0"}}

    def mock_get(*args, **kwargs):  # we pass URL and timeout to get function
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    assert _get_latest_pysparkgui_version() == Version("1.10.0")


def test_should_show_new_version_notification_skip(monkeypatch):
    monkeypatch.setattr(pysparkgui.config, "SHOW_NEW_VERSION_NOTIFICATION", False)
    assert _should_show_new_version_notification() == False
