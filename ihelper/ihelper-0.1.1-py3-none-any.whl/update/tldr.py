import click
from ishutils.common.run import run


@click.command(name="tldr")
def main() -> None:
    run(args=["tldr", "--update"])
