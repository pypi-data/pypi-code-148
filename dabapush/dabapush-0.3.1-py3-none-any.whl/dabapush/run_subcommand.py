"""Some module documentation
"""

import click
from loguru import logger as log
from .Dabapush import Dabapush


@click.command(help="Run dabapush job in the current working directory.")
@click.argument("targets", nargs=-1)
@click.pass_context
def run(ctx, targets: list[str]) -> None:
    """run verb

    Parameters
    ----------
    ctx :
        param targets: list[str]:
    targets :
        list[str]:
    targets: list[str] :


    Returns
    -------

    """
    db: Dabapush = ctx.obj
    log.debug(f"Running DabaPush job in {db.working_dir}")
    # log.debug(f'Using this global configuration {db.global_config}')
    # log.debug(f'Using this local configuration {db.config}')

    db.jb_run(targets)
