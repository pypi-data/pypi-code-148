import click
from ishutils.common.remove import remove
from ishutils.ubuntu import DESKTOP_FILE_INSTALL_DIR

from .. import OPT
from . import NAME


@click.command(name=NAME)
def main() -> None:
    remove(OPT / NAME)
    remove(DESKTOP_FILE_INSTALL_DIR / f"{NAME}.desktop")
