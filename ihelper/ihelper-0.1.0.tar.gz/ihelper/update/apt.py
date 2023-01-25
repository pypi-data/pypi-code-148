import click
from ishutils.common.run import run


@click.command(name="apt")
def main() -> None:
    run(args=["sudo", "apt", "update"])
    run(args=["sudo", "apt", "full-upgrade"])
