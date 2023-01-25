import click
from ishutils.common.run import run


@click.command(name="snap")
def main() -> None:
    run(args=["sudo", "snap", "refresh"])
