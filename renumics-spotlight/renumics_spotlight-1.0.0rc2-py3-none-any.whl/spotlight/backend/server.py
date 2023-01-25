"""
Setup for Spotlight server and browser.
"""

import contextlib
import inspect
import os
import threading
import time
import socket
from pathlib import Path
from typing import Optional, Union, Dict, Type

import click
import pandas as pd
import uvicorn
from typing_extensions import Literal

from renumics.spotlight.typing import PathType
from renumics.spotlight.dataset.typing import ColumnType
from .app import create_app
from .layout import _LayoutLike, parse


def find_free_port() -> int:
    """Find are free port between 1024 and 65535"""
    with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.bind(("", 0))
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return sock.getsockname()[1]


def is_port_in_use(port: int) -> bool:
    """check if port is already in use"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        return sock.connect_ex(("localhost", port)) == 0


class Server(uvicorn.Server):
    """
    Our custom Uvicorn server.
    """

    def install_signal_handlers(self) -> None:
        ...

    def run_in_thread(self) -> threading.Thread:
        """
        Run Uvicorn in separate thread.
        """
        thread = threading.Thread(target=self.run, daemon=True)
        thread.start()
        time.sleep(0.1)
        # Wait 2 seconds for server to start.
        for _ in range(20):
            if self.started:
                return thread
            if not thread.is_alive():
                break
            time.sleep(0.1)
        raise RuntimeError("Spotlight not started.")


def setup(
    table_or_folder: Optional[PathType],
    dtype: Optional[Dict[str, Type[ColumnType]]] = None,
    host: str = "localhost",
    port: Union[int, str] = "auto",
    layout: Optional[_LayoutLike] = None,
    log_level: Union[
        int, Literal["trace", "debug", "info", "warning", "error", "critical"]
    ] = "info",
) -> Server:
    """
    Prepare Renumics Spotlight server for launching.
    """
    # pylint: disable=too-many-arguments
    df_to_serve = None

    if table_or_folder is not None:
        supported_extensions = (".h5", ".csv")

        # dataframe support
        if isinstance(table_or_folder, pd.DataFrame):
            df_to_serve = table_or_folder
            os.environ["SPOTLIGHT_TABLE_FILE"] = "__df_in_memory__"

        # file support
        elif Path(table_or_folder).is_file():
            if Path(table_or_folder).suffix in supported_extensions:
                os.environ["SPOTLIGHT_TABLE_FILE"] = str(table_or_folder)
            else:
                raise click.BadArgumentUsage(
                    inspect.cleandoc(
                        f"""
                        Invalid file extension!
                          Supported: {", ".join(supported_extensions)}
                        """
                    )
                )

        else:  # folder
            os.environ["SPOTLIGHT_TABLE_FILE"] = str(table_or_folder)

    elif "SPOTLIGHT_TABLE_FILE" not in os.environ:
        os.environ["SPOTLIGHT_TABLE_FILE"] = str(Path.cwd())

    app = create_app(layout=None if layout is None else parse(layout))
    if df_to_serve is not None:
        app.data_source.open_dataframe(df_to_serve, dtype)  # type: ignore

    if port == "auto":
        port_number = find_free_port()
    else:
        port_number = int(port)

    config = uvicorn.Config(
        app,
        host=host,
        port=port_number,
        log_level=log_level,
        ws="wsproto",
        workers=4,
        reload=os.environ.get("SPOTLIGHT_DEV") == "true",
    )
    server = Server(config)
    return server
