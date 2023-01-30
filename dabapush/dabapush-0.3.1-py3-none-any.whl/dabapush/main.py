""""""

import sys
import click
from loguru import logger as log

from .create_subcommand import create
from .run_subcommand import run
from .update_subcommand import update
from .reader_subcommand import reader
from .writer_subcommand import writer
from .Dabapush import Dabapush


@click.group()
@click.option("--logfile", help="file to log in (optional)")
@click.option("--loglevel", default="INFO", help="the level to log, yk")
@click.pass_context
def cli(ctx: click.Context, logfile, loglevel):
    """

    Parameters
    ----------
    ctx :
        param logfile:
    loglevel :
        param ctx: click.Context:
    ctx :
        click.Context:
    ctx: click.Context :

    logfile :


    Returns
    -------

    """
    # prepare log options
    log.remove()

    if logfile is not None:
        if loglevel is None:
            loglevel = "DEBUG"
            log.add(sys.stdout, level = loglevel)
        log.add(logfile, level = loglevel)
    # do standard logging into STDOUT
    else:
        log.add(sys.stdout, level = 'DEBUG')
    # prepare context
    ctx.ensure_object(Dabapush)

    db: Dabapush = ctx.obj
    log.debug(f"Starting DabaPush in {db.working_dir} from {db.install_dir}")


cli.add_command(reader)
cli.add_command(writer)
cli.add_command(run)
cli.add_command(create)
cli.add_command(update)

if __name__ == "__main__":
    cli(obj=Dabapush())
