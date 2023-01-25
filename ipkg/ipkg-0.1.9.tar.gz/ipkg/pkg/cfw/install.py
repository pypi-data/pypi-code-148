import typing
from pathlib import Path
from tempfile import TemporaryDirectory

import click
import requests
from ishutils.common.download import download
from ishutils.common.extract import extract
from ishutils.common.replace import replace
from ishutils.ubuntu.desktop import DesktopEntry, make_desktop_file

from .. import DOWNLOADS, OPT
from . import DOWNLOAD_URL, LOGO_URL, NAME, RELEASE_API


@click.command(name=NAME)
def main(version: typing.Optional[str] = None) -> None:
    if not version:
        json = requests.get(url=RELEASE_API).json()
        version = json["tag_name"]
    filename: str = f"Clash.for.Windows-{version}-x64-linux.tar.gz"
    url: str = f"{DOWNLOAD_URL}/{version}/{filename}"
    filepath: Path = DOWNLOADS / filename
    download(url=url, output=filepath)
    with TemporaryDirectory() as tmp_dir:
        extract(src=filepath, dst=tmp_dir)
        replace(
            src=Path(tmp_dir) / f"Clash for Windows-{version}-x64-linux", dst=OPT / NAME
        )
    logo_path = OPT / NAME / "logo.png"
    download(url=LOGO_URL, output=logo_path)
    make_desktop_file(
        slug=NAME,
        entry=DesktopEntry(
            Name="Clash for Windows",
            Exec=str(OPT / NAME / "cfw"),
            Icon=str(logo_path),
        ),
    )
