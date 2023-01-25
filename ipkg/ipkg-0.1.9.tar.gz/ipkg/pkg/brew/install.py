import os
import tempfile
from pathlib import Path

import click
from ishutils.common.remove import remove
from ishutils.common.run import run

from .. import SHELL
from . import (
    HOMEBREW_BOTTLE_DOMAIN,
    HOMEBREW_BREW_GIT_REMOTE,
    HOMEBREW_BREW_INSTALL_GIT_REMOTE,
    HOMEBREW_CORE_GIT_REMOTE,
    NAME,
)


@click.command(name=NAME)
def main():
    tmpdir: Path = Path(tempfile.mkdtemp())
    run(
        args=[
            "git",
            "clone",
            "--depth",
            "1",
            HOMEBREW_BREW_INSTALL_GIT_REMOTE,
            tmpdir,
        ]
    )
    os.environ["HOMEBREW_BREW_GIT_REMOTE"] = HOMEBREW_BREW_GIT_REMOTE
    os.environ["HOMEBREW_CORE_GIT_REMOTE"] = HOMEBREW_CORE_GIT_REMOTE
    os.environ["HOMEBREW_BOTTLE_DOMAIN"] = HOMEBREW_BOTTLE_DOMAIN
    run(args=[SHELL, tmpdir / "install.sh"])
    remove(tmpdir)
