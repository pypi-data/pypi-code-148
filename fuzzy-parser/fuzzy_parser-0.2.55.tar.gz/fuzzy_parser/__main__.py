import sys

from fuzzy_parser.engine import Engine


def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]
    expression = next(iter(args), None)
    (dates, traces) = Engine().when(expression)
    print(dates)
    print(traces)


if __name__ == "__main__":
    sys.exit(main())

