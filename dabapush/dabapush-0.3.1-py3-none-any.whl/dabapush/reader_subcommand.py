from typing import List
import click
from loguru import logger as log
from .Dabapush import Dabapush

# Reader
@click.group()
@click.pass_context
def reader(ctx):
    """

    Parameters
    ----------
    ctx :


    Returns
    -------

    """
    pass


@reader.command(help="Add a reader to the project.")
@click.option(
    "--parameter",
    "-p",
    multiple=True,
    help="supply additional configuration detail for the reader in a key value format, e.g. pattern='*.ndjson'. Can occur multiple times.",
)
@click.argument("type")
@click.argument("name")
@click.pass_context
def add(ctx: click.Context, parameter: list[str], type: str, name: str) -> None:
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
    db.rd_add(type, name)
    db.rd_update(name, params)
    db.pr_write()


@reader.command()
@click.argument("name")
@click.pass_context
def remove(ctx, name):
    """

    Parameters
    ----------
    ctx :
        click.Context : click's context
    name :
        str : name of the reader to remove

    Returns
    -------

    """
    db: Dabapush = ctx.obj
    db.rd_rm(name)


@reader.command(help="lists all available reader plugins")
@click.pass_context
def list(ctx):
    """

    Parameters
    ----------
    ctx :


    Returns
    -------

    """
    readers = ctx.obj.rd_list()
    for key in readers:
        click.echo(f"- {key}:\t")


@reader.command(help="Configure the reader with given name")
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
    db.rd_update(name, params)
    db.pr_write()


# @reader.command(help='register a reader class plugin')
# @click.argument('name')
# @click.argument('path', type=click.Path(dir_okay=False, exists=True))
# @click.option('--global', '-g', help='register globally, files are copied into plugin folder', default=False)
# def register():
#     """ """
#     # branch if global
#         # check wether class is valid, i.e. is a descendant of Reader
#         # copy to source file pluginfolder (is that a good idea?)
#         # rewrite global conf with updated plugin registry
#     # branch if local
#         # check wether class is valid
#         # rewrite local configuration with a plugin registry
#     pass

# @reader.command(help='unregister a reader class plugin')
# @click.argument('name')
# @click.option('--global', '-g', help='register globally, files are copied into plugin folder', default=False)
# def unregister():
#     """ """
#     # branch if global
#         # check wether name exists in registry
#         # delete source file from pluginfolder (is that a good idea?)
#         # rewrite global conf with updated plugin registry
#     # branch if local
#         # check wether name exists in registry
#         # rewrite local configuration with a plugin registry
#     pass
