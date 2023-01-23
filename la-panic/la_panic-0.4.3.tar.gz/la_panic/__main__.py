import click
import coloredlogs
import logging

from la_panic.panic_parser.panic_parser import cli as parser_cli


coloredlogs.install(level=logging.DEBUG)


def cli():
    cli_commands = click.CommandCollection(sources=[
        parser_cli
    ])
    cli_commands()


if __name__ == '__main__':
    cli()
