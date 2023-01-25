import os
from pathlib import Path

import click
from ishutils.common.run import run


@click.command(name="ssh")
@click.option(
    "-p", "--prefix", type=click.Path(file_okay=False, dir_okay=True), default="gpg"
)
def main(prefix: str | Path) -> None:
    prefix = Path(prefix)
    os.makedirs(name=prefix, exist_ok=True)
    run(
        args=[
            "gpg",
            "--export-secret-keys",
            "--armor",
            "--output",
            prefix / "secret.asc",
        ]
    )
