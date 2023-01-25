import click

from ...utils.cache import open_cache, unset
from . import NAME


@click.command(name=NAME)
def main() -> None:
    with open_cache() as cache:
        unset(cache=cache, names=["LD_LIBRARY_PATH"])
