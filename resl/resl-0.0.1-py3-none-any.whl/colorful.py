"""
resl.colorful
-------------

People like colors in their scripts, right?
"""

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'


def cprint(string, color):
    """Will print a string with a color!

    If you want to print a string with more than 1 color,
    you can just use, for example:

    >> import colorful
    >> from colorful import cprint
    >>
    >>
    >> cprint("hello world!", colorful.OKGREEN + colorful.UNDERLINE + colorful.BOLD)

    Args:
        string - the string that will be printed
        color  - a color constant (defined inside colorful)
    """

    print(f"{color}{string}{ENDC}")


def cinput(string, color):
    """Will prompt a colorized input message."""

    return input(
        f"{color}{string}{ENDC}"
    )
