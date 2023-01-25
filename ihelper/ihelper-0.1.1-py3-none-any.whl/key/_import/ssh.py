from pathlib import Path

import click
from ishutils.common.copy import copy

from ..typing import SSH_TYPES


@click.command(name="gpg")
@click.option(
    "-p",
    "--prefix",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    default="ssh",
)
def main(prefix: str | Path) -> None:
    prefix = Path(prefix)
    config_path: Path = prefix / "config"
    if config_path.exists():
        copy(src=config_path, dst=Path.home() / ".ssh" / "config")
    for ssh_type in SSH_TYPES:
        private_key_name: str = f"id_{ssh_type}"
        private_key_path: Path = prefix / private_key_name
        if private_key_path.exists():
            copy(src=private_key_path, dst=Path.home() / ".ssh" / private_key_name)
        public_key_name: str = f"id_{ssh_type}.pub"
        public_key_path: Path = prefix / public_key_name
        if public_key_path.exists():
            copy(src=public_key_path, dst=Path.home() / ".ssh" / public_key_name)
