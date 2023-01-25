#!/usr/bin/env python3
"""
    Command line entrypoint for the renumics-spotlight python package
"""
import multiprocessing
import signal
import sys
from typing import Any, Optional, Union

import click

from renumics.spotlight import __version__
from renumics.spotlight.webbrowser import launch_browser_in_thread
from renumics.spotlight.backend.server import setup


@click.command()
@click.argument(
    "table-or-folder",
    type=click.Path(exists=True),
    required=False,
)
@click.option(
    "--host",
    "-h",
    default="localhost",
    help="The host that Spotlight should listen on.",
    show_default=True,
)
@click.option(
    "--port",
    "-p",
    type=str,
    default="auto",
    help="The port that Spotlight should listen on (use 'auto' to use a random free port)",
    show_default=True,
)
@click.option(
    "--no-browser",
    is_flag=True,
    default=False,
    help="Do not automatically show Spotlight in browser.",
)
@click.option(
    "--layout",
    type=click.Path(exists=True, dir_okay=False),
    default=None,
    help="Preconfigured layout to use as default.",
)
@click.version_option(__version__)
def main(
    table_or_folder: str,
    host: str,
    port: Union[int, str],
    layout: Optional[str],
    no_browser: bool,
) -> None:
    """
    Parse CLI arguments and launch Renumics Spotlight.
    """
    server = setup(table_or_folder, None, host, port, layout)

    def _sigint_handler(*_args: Any) -> None:
        if server.should_exit:
            sys.tracebacklimit = 0
            processes = multiprocessing.active_children()
            for process in processes:
                process.terminate()
        server.should_exit = True

    signal.signal(signal.SIGINT, _sigint_handler)

    if not no_browser:
        launch_browser_in_thread(server.config.host, server.config.port)
    server.run()
