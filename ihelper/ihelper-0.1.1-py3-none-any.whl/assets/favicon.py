import os
import string
from pathlib import Path

import click
from ishutils.common.download import download
from ishutils.common.run import run

from .typing import FONT_AWESOME_URL


@click.command(name="favicon")
@click.option("-c", "--color", default="cyan")
@click.option(
    "-o",
    "--output",
    type=click.Path(file_okay=False, dir_okay=True),
    default="favicon",
)
def main(color: str, output: str | Path) -> None:
    output = Path(output)
    for format in ["svg", "png", "ico"]:
        os.makedirs(name=output / format, exist_ok=True)
    for letter in string.ascii_lowercase:
        svg: Path = output / "svg" / f"{letter}.svg"
        png: Path = output / "png" / f"{letter}.png"
        ico: Path = output / "ico" / f"{letter}.ico"
        download(url=FONT_AWESOME_URL + f"/solid/{letter}.svg", output=svg)
        args = [
            "magick",
            "convert",
            "-background",
            "none",
            svg,
            "-fill",
            color,
            "-colorize",
            "100",
            "-resize",
            "512x512",
            "-gravity",
            "center",
            "-extent",
            "512x512",
        ]
        run(args=[*args, png])
        run(args=[*args, "-resize", "128x128", ico])
