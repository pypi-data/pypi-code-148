import click
from ishutils.common.remove import remove
from ishutils.ubuntu.desktop import DESKTOP_FILE_INSTALL_DIR

from .. import OPT
from . import NAME


@click.command(name=NAME)
def main() -> None:
    remove(path=OPT / NAME)
    remove(path=DESKTOP_FILE_INSTALL_DIR / (NAME + ".desktop"))
