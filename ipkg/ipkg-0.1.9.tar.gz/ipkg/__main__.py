import logging
from pathlib import Path

import click
from ishutils.logging import install as logging_install

from . import __version__, pkg
from .cmd.cache import main as cmd_cache
from .cmd.install import main as cmd_install
from .cmd.list import main as cmd_list
from .cmd.load import main as cmd_load
from .cmd.post_install import main as cmd_post_install
from .cmd.remove import main as cmd_remove
from .cmd.shell_env import main as cmd_shell_env
from .cmd.unload import main as cmd_unload


@click.group(name="ipkg", context_settings={"show_default": True})
@click.version_option(version=__version__)
@click.option(
    "--log-level",
    type=click.Choice(
        choices=list(logging.getLevelNamesMapping().keys()),
        case_sensitive=False,
    ),
    default="INFO",
)
@click.option(
    "--downloads",
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    default=Path.home() / "Downloads",
)
@click.option(
    "--shell",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, executable=True),
    default="/bin/bash",
)
def main(log_level: str, shell: str | Path, downloads: str | Path):
    log_level = log_level.upper()
    logging_install(level=logging.getLevelName(level=log_level))
    pkg.DOWNLOADS = Path(downloads)
    pkg.SHELL = Path(shell)


main.add_command(cmd=cmd_cache)
main.add_command(cmd=cmd_install)
main.add_command(cmd=cmd_list)
main.add_command(cmd=cmd_load)
main.add_command(cmd=cmd_post_install)
main.add_command(cmd=cmd_remove)
main.add_command(cmd=cmd_shell_env)
main.add_command(cmd=cmd_unload)


if __name__ == "__main__":
    main(prog_name=main.name)
