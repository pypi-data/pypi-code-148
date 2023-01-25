import click
from ishutils.common.download import download
from ishutils.common.run import run

from .. import DOWNLOADS, SHELL
from . import KEY_PATH, KEY_URL, NAME, SOURCES_LIST, SOURCES_LIST_PATH


@click.command(name=NAME)
def main() -> None:
    key_filename: str = NAME + ".asc"
    key_filepath = DOWNLOADS / key_filename
    download(url=KEY_URL, output=key_filepath)
    run(args=["sudo", "cp", str(key_filepath), str(KEY_PATH)])
    run(
        args=[
            "sudo",
            SHELL,
            "-c",
            f'echo "{SOURCES_LIST}" > "{SOURCES_LIST_PATH}"',
        ]
    )
    run(args=["sudo", "apt", "update"])
    run(args=["sudo", "apt", "install", NAME])
