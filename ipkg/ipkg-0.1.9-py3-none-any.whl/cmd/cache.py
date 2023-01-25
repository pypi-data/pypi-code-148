import click
from ishutils.common.remove import remove
from rich import print

from ..utils.cache import CACHE_DIR


@click.command(name="clean")
def clean() -> None:
    remove(CACHE_DIR)


@click.command(name="prefix")
def prefix() -> None:
    print(CACHE_DIR)


@click.group(name="cache", invoke_without_command=True)
@click.pass_context
def main(ctx: click.Context) -> None:
    if not ctx.invoked_subcommand:
        ctx.invoke(prefix)


main.add_command(cmd=clean)
main.add_command(cmd=prefix)
