import click

from ..pkg.llvm.unload import main as llvm
from ..utils import cache


@click.group(name="unload")
@click.option("--dry-run", is_flag=True)
def main(dry_run: bool) -> None:
    cache.DRY_RUN = dry_run
    pass


main.add_command(cmd=llvm)
