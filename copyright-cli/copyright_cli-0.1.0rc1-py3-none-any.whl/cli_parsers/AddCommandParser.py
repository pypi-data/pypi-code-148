import os.path

from .. import copyright
from . import DebugParser


def _execute_add(args):
    copyright.add_copyright(args.path, args.output, args.check)


def setup_command(subparsers):
    parser = subparsers.add_parser("add", help='''
        Adds copyright information to a file''')
    parser.set_defaults(command_func=lambda args: _execute_add(args))

    parser.add_argument("path", nargs='?', default=".",
                        type=os.path.abspath,
                        help="Path to a folder containing a copyright.toml file.")
    parser.add_argument("--output",
                        type=os.path.abspath,
                        help="Path to a folder to which the updated files will be put. "
                             "If not provided, files will be updated in place")
    parser.add_argument("--no-check", dest='check', default=True, action='store_false',
                        help="Don't check if the copyright test already exists in the file, always add it.")

    DebugParser.setup(parser)
