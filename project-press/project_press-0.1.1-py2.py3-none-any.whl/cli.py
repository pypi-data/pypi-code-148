import sys

from imxdparser import ChildParser, MainParser

from .clone import clone
from .validate import validate


def parser_error(parser, argv, *_args):
    # Reparse with an additional parameter to force an error
    argv += [""]
    parser.parse_args(argv)


def options(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    def error(*_args):
        parser_error(parser, argv)

    parser = MainParser(description="Lorem ipsum sit dolor amet")
    parser.attach()
    parser.set_defaults(func=error)

    subparser = ChildParser(parser, "validate")
    subparser.add_argument("template")
    subparser.attach()
    subparser.set_defaults(func=validate)

    subparser = ChildParser(parser, "clone")
    subparser.add_argument("-o", "--output", default=".")
    subparser.add_argument("template")
    subparser.attach()
    subparser.set_defaults(func=clone)

    return vars(parser.parse_args(argv))


def main():
    args = options()
    if args.get("func"):
        func = args.pop("func")
        func(args)
