from pathlib import Path
from tempfile import TemporaryDirectory

import click
from ishutils.common.download import download
from ishutils.common.extract import extract
from ishutils.common.replace import replace
from ishutils.ubuntu.desktop import DesktopEntry, make_desktop_file

from .. import DOWNLOADS, OPT
from . import NAME, VERSION_TO_FILENAME


@click.command(name=NAME)
@click.option(
    "-v",
    "--version",
    type=click.Choice(choices=list(VERSION_TO_FILENAME.keys())),
    default="2.3.3.0",
)
def main(version: str) -> None:
    filename: str = VERSION_TO_FILENAME[version]
    url: str = f"https://redirector.gvt1.com/edgedl/android/studio/ide-zips/{version}/{filename}"
    filepath: Path = DOWNLOADS / filename
    download(url=url, output=DOWNLOADS / filename)
    with TemporaryDirectory() as tmp_dir:
        extract(src=filepath, dst=tmp_dir)
        dst: Path = OPT / NAME / version
        replace(src=Path(tmp_dir) / NAME, dst=dst)
    make_desktop_file(
        slug=f"{NAME}-{version}",
        entry=DesktopEntry(
            Name=f"Android Studio {version}",
            Exec=str(dst / "bin" / "studio.sh"),
            Icon=str(dst / "bin" / "studio.png"),
        ),
    )
