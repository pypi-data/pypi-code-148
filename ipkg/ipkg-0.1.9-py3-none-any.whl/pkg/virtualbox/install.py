from pathlib import Path

import click
from ishutils.common.download import download
from ishutils.common.run import run

from .. import DOWNLOADS
from . import KEY_NAME, KEY_URL, NAME


@click.command(name=NAME, help="https://www.virtualbox.org/wiki/Linux_Downloads")
def main() -> None:
    key_path: Path = DOWNLOADS / KEY_NAME
    download(url=KEY_URL, output=key_path)
    run(
        args=[
            "sudo",
            "gpg",
            "--dearmor",
            "--output",
            "/etc/apt/trusted.gpg.d/oracle-virtualbox-2016.gpg",
            key_path,
        ]
    )
    codename: str = str(
        run(args=["lsb_release", "--codename", "--short"], capture_output=True).stdout,
        encoding="utf-8",
    ).strip()
    sources_list: str = (
        f"deb https://download.virtualbox.org/virtualbox/debian {codename} contrib"
    )
    run(
        args=[
            "sudo",
            "bash",
            "-c",
            f'echo "{sources_list}" > /etc/apt/sources.list.d/virtualbox.list',
        ]
    )
    run(args=["sudo", "apt", "update"])
    run(args=["sudo", "apt", "install", "virtualbox-6.1"])
