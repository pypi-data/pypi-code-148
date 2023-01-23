import base64
import os
import pickle
import subprocess
from collections.abc import Callable
from pathlib import Path
from typing import ParamSpec
from urllib.parse import urlencode


PLUGIN_PATH = Path(os.environ.get('SWIFTBAR_PLUGIN_PATH', '.'))


P = ParamSpec('P')


def serialize_callback(callback: Callable[P, object], *args: P.args, **kwargs: P.kwargs) -> str:
    cb_byt = pickle.dumps((callback, args, kwargs))
    cb_b64 = base64.b64encode(cb_byt)
    cb_txt = cb_b64.decode('ascii')
    return cb_txt


def deserialize_callback(cb_txt: str) -> tuple[Callable[P, object], P.args, P.kwargs]:
    cb_b64 = cb_txt.encode('ascii')
    cb_byt = base64.b64decode(cb_b64)
    callback, args, kwargs = pickle.loads(cb_byt)
    return callback, args, kwargs


def open_url(url: str, **params: str | int | None) -> subprocess.CompletedProcess[bytes]:
    clean_params = urlencode({k:v for k,v in params.items() if v is not None})
    if clean_params:
        url = f'{url}?{clean_params}'
    cmd = ['open', '-g', url]
    return subprocess.run(cmd, capture_output=True, check=True)


def refreshplugin() -> subprocess.CompletedProcess[bytes]:
    return open_url('swiftbar://refreshplugin', name=PLUGIN_PATH.name)


def refreshallplugins() -> subprocess.CompletedProcess[bytes]:
    return open_url('swiftbar://refreshallplugins')


def enableplugin() -> subprocess.CompletedProcess[bytes]:
    return open_url('swiftbar://enableplugin', name=PLUGIN_PATH.name)


def disableplugin() -> subprocess.CompletedProcess[bytes]:
    return open_url('swiftbar://disableplugin', name=PLUGIN_PATH.name)


def toggleplugin() -> subprocess.CompletedProcess[bytes]:
    return open_url('swiftbar://toggleplugin', name=PLUGIN_PATH.name)


def notify(**params: str | int | None) -> subprocess.CompletedProcess[bytes]:
    return open_url('swiftbar://notify', name=PLUGIN_PATH.name, **params)


def copy_to_clipboard(data: str | bytes) -> None:
    if isinstance(data, str):
        data = data.encode()
    subprocess.run(['pbcopy'], input=data, check=True)
