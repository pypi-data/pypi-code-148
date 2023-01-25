import click
from ishutils.common.run import run

from . import NAME


@click.command(name=NAME)
def main() -> None:
    run(args=["gh", "auth", "login"])
    run(args=["gh", "auth", "setup-git"])
