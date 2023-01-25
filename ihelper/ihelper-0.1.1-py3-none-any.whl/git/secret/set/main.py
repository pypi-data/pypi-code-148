import click

from .pypi import main as cmd_pypi


@click.group(name="set")
def main() -> None:
    pass


main.add_command(cmd=cmd_pypi)
