from pathlib import Path

import click
from ishutils.common.run import run


@click.command(name="gpg")
@click.option(
    "-p",
    "--prefix",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    default="gpg",
)
def main(prefix: str | Path) -> None:
    prefix = Path(prefix)
    run(args=["gpg", "--import", prefix / "secret.asc"])
    signing_key: str = str(
        run(args=["git", "config", "user.signingKey"], capture_output=True).stdout,
        encoding="utf-8",
    ).strip()
    run(args=["gpg", "--edit-key", signing_key, "trust"])
