import os
from pathlib import Path
from tempfile import TemporaryDirectory

import click
from ishutils.common.download import download
from ishutils.common.extract import extract
from ishutils.common.replace import replace

from .. import BIN, DOWNLOADS
from . import NAME


@click.command(
    name=NAME, help="https://github.com/libthu/reserves-lib-tsinghua-downloader"
)
def main():
    filename: str = "downloader-ubuntu-latest-py3.9.zip"
    filepath: Path = DOWNLOADS / filename
    download(
        url="https://github.com/libthu/reserves-lib-tsinghua-downloader/releases/latest/download/downloader-ubuntu-latest-py3.9.zip",
        output=filepath,
    )
    with TemporaryDirectory() as tmp_dir:
        extract(src=filepath, dst=tmp_dir)
        replace(src=Path(tmp_dir) / "downloader", dst=BIN / NAME)
        mode = os.stat(path=BIN / NAME).st_mode
        mode |= (mode & 0o444) >> 2
        exec: Path = BIN / NAME
        exec.chmod(mode=mode)
