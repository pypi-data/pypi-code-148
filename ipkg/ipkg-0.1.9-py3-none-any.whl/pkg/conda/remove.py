from pathlib import Path

import click
from ishutils.common.remove import remove

from . import DEFAULT_PREFIX, HELP_PREFIX, NAME


@click.command(
    name=NAME,
    help="https://conda.io/projects/conda/en/latest/user-guide/install/macos.html#uninstalling-anaconda-or-miniconda",
)
@click.option(
    "-p",
    "--prefix",
    "--path",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    default=DEFAULT_PREFIX,
    help=HELP_PREFIX,
)
def main(prefix: str | Path) -> None:
    remove(prefix)
    remove(Path.home() / ".condarc")
    remove(Path.home() / ".conda")
    remove(Path.home() / ".continuum")
