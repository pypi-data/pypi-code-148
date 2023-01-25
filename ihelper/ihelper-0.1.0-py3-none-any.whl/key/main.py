import click

from ._import.main import main as cmd_import
from .export.main import main as cmd_export


@click.group(name="key")
def main() -> None:
    pass


main.add_command(cmd=cmd_export)
main.add_command(cmd=cmd_import)
