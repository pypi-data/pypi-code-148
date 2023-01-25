import click
from ishutils.common.run import run


@click.command(name="ignore-io")
def main() -> None:
    run(args=["git", "ignore-io", "--update-list"])
