from typing import List
import click

from .Dabapush import Dabapush

# Writer
@click.group()
def writer():
    """ """
    pass


@writer.command()
@click.option(
    "--parameter",
    "-p",
    multiple=True,
    help="supply additional configuration detail for the writer in a key value format, e.g. port=1234. Can occur multiple times.",
)
@click.argument("type")
@click.argument("name")
@click.pass_context
def add(ctx: click.Context, parameter: list[str], type: str, name: str):
    """

    Parameters
    ----------
    ctx :
        param name:
    type :

    name :


    Returns
    -------
    type None:

    """
    params = dict(arg.split("=") for arg in parameter)
    db: Dabapush = ctx.obj
    db.wr_add(type, name)
    db.wr_update(name, params)
    db.pr_write()


@writer.command()
@click.argument("name")
@click.pass_context
def remove(ctx: click.Context, name: str):
    """ """
    db: Dabapush = ctx.obj
    db.rd_rm(name)


@writer.command()
@click.pass_context
def list(ctx):
    """

    Parameters
    ----------
    ctx :


    Returns
    -------

    """
    writers = ctx.obj.wr_list()
    for key in writers:
        click.echo(f"- {key}:\t")


@writer.command(help="Configure the writer with given name")
@click.option(
    "--parameter",
    "-p",
    multiple=True,
    type=click.STRING,
    help="supply additional configuration detail for the reader in a key value format, e.g. pattern='*.ndjson'. Can occur multiple times",
)
@click.argument("name")
@click.pass_context
def configure(ctx: click.Context, parameter: List[str], name: str):
    """

    Parameters
    ----------
    ctx :
        param name:
    path :
        param recursive:
    pattern :

    name :

    recursive :


    Returns
    -------

    """

    params = dict(arg.split("=") for arg in parameter)
    db: Dabapush = ctx.obj
    db.wr_update(name, params)
    db.pr_write()
