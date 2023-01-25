import logging

import click
from ishutils.config import config
from ishutils.logging import install

from . import __version__
from .assets.main import main as cmd_assets
from .git.main import main as cmd_git
from .key.main import main as cmd_key
from .update.main import main as cmd_update


@click.group(name="ihelper", context_settings={"show_default": True})
@click.option(
    "--log-level",
    type=click.Choice(choices=list(logging.getLevelNamesMapping().keys())),
    default=logging.getLevelName(logging.INFO),
)
@click.option("-y", "--yes", is_flag=True)
@click.version_option(version=__version__)
def main(log_level: str, yes: bool) -> None:
    install(level=logging.getLevelName(log_level))
    config.yes = yes


main.add_command(cmd=cmd_assets)
main.add_command(cmd=cmd_git)
main.add_command(cmd=cmd_key)
main.add_command(cmd=cmd_update)


if __name__ == "__main__":
    main()
