from pathlib import Path

import click
from ishutils.common.download import download
from ishutils.common.run import run

from .. import DOWNLOADS
from . import GET_DOCKER_URL, NAME


@click.command(
    name=NAME,
    help="https://docs.docker.com/engine/install/ubuntu/#install-using-the-convenience-script",
)
def main() -> None:
    url: str = GET_DOCKER_URL
    filename: str = "get-docker.sh"
    filepath: Path = DOWNLOADS / filename
    download(url=url, output=filepath)
    run(args=["sudo", "bash", filepath])
    run(args=["sudo", "apt", "install", "uidmap"])
    run(args=["dockerd-rootless-setuptool.sh", "install"])
