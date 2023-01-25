from pathlib import Path

import click
from ishutils.common.link import link

from .. import BIN
from . import NAME


@click.command(name=NAME)
def main() -> None:
    link(
        src=Path.home() / "Android" / "Sdk" / "platform-tools" / "adb", dst=BIN / "adb"
    )
