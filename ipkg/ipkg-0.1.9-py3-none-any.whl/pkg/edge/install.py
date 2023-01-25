import click
from ishutils.common.download import download
from ishutils.common.run import run

from .. import DOWNLOADS, SHELL
from . import KEY_NAME, KEY_URL, NAME, SOURCES_LIST, SOURCES_LIST_PATH, TRUSTED_KEY_PATH


@click.command(name=NAME)
def main() -> None:
    key_path = DOWNLOADS / KEY_NAME
    download(url=KEY_URL, output=key_path)
    run(
        args=[
            "sudo",
            "gpg",
            "--dearmor",
            "--output",
            TRUSTED_KEY_PATH,
            key_path,
        ]
    )
    run(
        args=[
            "sudo",
            SHELL,
            "-c",
            f'echo "{SOURCES_LIST}" > "{SOURCES_LIST_PATH}"',
        ]
    )
    run(args=["sudo", "apt", "update"])
    run(args=["sudo", "apt", "install", "microsoft-edge-stable"])
