import click

from ..pkg.conda.load import main as conda
from ..pkg.docker.load import main as docker
from ..pkg.llvm.load import main as llvm
from ..utils import cache


@click.group(name="load")
@click.option("--dry-run", is_flag=True)
def main(dry_run: bool) -> None:
    cache.DRY_RUN = dry_run


main.add_command(cmd=conda)
main.add_command(cmd=docker)
main.add_command(cmd=llvm)
