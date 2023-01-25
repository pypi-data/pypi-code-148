import click

from .delete.main import main as cmd_delete
from .set.main import main as cmd_set


@click.group(name="secret")
def main() -> None:
    pass


main.add_command(cmd=cmd_delete)
main.add_command(cmd=cmd_set)
