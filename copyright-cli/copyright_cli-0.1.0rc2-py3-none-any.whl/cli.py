from copyright_cli.cli_parsers import ArgumentParser
from copyright_cli.cli_parsers import AddCommandParser
import logging
import sys


__version = "0.1.0rc2"


def _setup_logging():
    logging.basicConfig(level=logging.DEBUG)


def _setup_parser():
    command = __package__.split('_')[0]
    parser = ArgumentParser(prog=command)
    parser.add_argument("-v", "--version", action="version", version=__version)

    subparsers = parser.add_subparsers(title="subcommand", dest="subcommand")
    subparsers.required = True

    AddCommandParser.setup_command(subparsers)

    return parser


def main(args=None):
    parser = _setup_parser()
    if not args:
        args = sys.argv[1:]

    parsed = parser.parse_args(args)
    if parsed.debug:
        _setup_logging()

    parsed.command_func(parsed)


if __name__ == '__main__':
    main()
