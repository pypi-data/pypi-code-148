from pathlib import Path

import click
from ishutils.common.remove import remove
from ishutils.common.run import run

from . import FONT_DIR, NAME


@click.command(name=NAME)
@click.option("--font-dir", type=click.Path(), default=FONT_DIR)
def main(font_dir: str | Path) -> None:
    remove(path=font_dir)
    run(args=["fc-cache", "--force"])
