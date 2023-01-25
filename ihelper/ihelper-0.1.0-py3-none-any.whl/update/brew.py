import click
from ishutils.common.run import run


@click.command(name="brew")
def main() -> None:
    run(args=["brew", "update"])
    run(args=["brew", "upgrade"])
