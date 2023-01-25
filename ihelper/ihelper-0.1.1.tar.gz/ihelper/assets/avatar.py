import os
from pathlib import Path

import click
from ishutils.common.download import download
from ishutils.common.run import run
from slugify import slugify

from .typing import AVATAR_URL


@click.command(name="avatar")
@click.option(
    "-o",
    "--output",
    type=click.Path(file_okay=False, dir_okay=True),
    default="avatar",
)
def main(output: str | Path) -> None:
    output = Path(output)
    os.makedirs(name=output / "jpg", exist_ok=True)
    os.makedirs(name=output / "png", exist_ok=True)
    for name, url in AVATAR_URL.items():
        name = slugify(name)
        jpg: Path = output / "jpg" / f"{name}.jpg"
        png: Path = output / "png" / f"{name}.png"
        download(url=url, output=jpg)
        run(args=["magick", "convert", jpg, png])
