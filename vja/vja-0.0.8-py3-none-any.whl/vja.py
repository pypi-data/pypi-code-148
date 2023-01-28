#!/usr/bin/env python

import logging
import webbrowser

import click
from click_aliases import ClickAliasedGroup

from vja import config, service

logger = logging.getLogger(__name__)

@click.group(cls=ClickAliasedGroup)
@click.option('-v', '--verbose', 'verbose', default=False, is_flag=True, help='verbose output')
def cli(verbose):
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
        logger.setLevel(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
        logger.setLevel(level=logging.INFO)


@cli.command(aliases=['list'], help='list relevant tasks (optionaly with -a)')
@click.option('-l', '--list', 'list')
@click.option('-a', '--all', 'list_size', count=True, help='show additional tasks (tomorrow + task without due date)')
@click.option('-i', '--urgency', 'urgency_sort', is_flag=True, help='sort by priority level')
def ls(list=None, list_size=0, urgency_sort=False):
    logger.info("list")
    service.list_tasks(list, list_size, urgency_sort)
    return

@cli.command(help='list new tasks')
def inbox(context=None, list_size=0):
    return


@cli.command(help='show task details')
@click.argument('task', required=True, type=click.INT)
def show(task):
    logger.debug("task: %s" % task.dict())
    print(task)

@cli.command(name='open', help='open task in browser')
@click.argument('task', required=False, type=click.INT)
def open_task(task):
    # TODO restore cache logic
    url = config.get_parser().get('application', 'frontend_url')
    if (task and task > 0):
        url += "/tasks/" + str(task)
    webbrowser.open_new_tab(url)


@cli.command(help='add new task, Example: \'add task do something .saturday @@context\'')
@click.argument('line', nargs=-1)
def add(line):
    return

@cli.command()
@click.argument('task', required=True, type=click.INT)
@click.argument('line', nargs=-1)
# @click.argument('modification', required=True, type=click.STRING)
def edit(task, line):
    return

@cli.command(help='mark task as complete')
@click.argument('task', required=True, type=click.INT)
def check(task):
    return

if __name__ == '__main__':
    cli()
