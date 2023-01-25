"""CLI v1 Argument Parser."""
import argparse
from ..__about__ import __package_name__ as _package_name

DESCRIPTION = "There's probably a fiesta somewhere."

class MyArgumentParser(argparse.ArgumentParser):

    def __init__(self, *args, **kwargs):
        super(MyArgumentParser, self).__init__(*args, **kwargs)

        self.error_message = ''
        self.result = ''

    def error(self, message):
        print("error: ", message)
        self.error_message = message

    def parse_args(self, *args, **kwargs):
        # catch SystemExit exception to prevent closing the application
        result = None
        if not args:
            self.error("invalid empty arguments")
            return result
        if args[0] is None or args[0] == "":
            self.error("invalid empty arguments")
            return result
        try:
            result = super().parse_args(*args, **kwargs)
        except SystemExit:
            pass
        self.result = result
        return result

    def get_parsed_args(self):
        return self.result

def create_argument_parser():
    # Create argument parser
    parser = MyArgumentParser(add_help=True, description=DESCRIPTION)

    # Add arguments to parser
    parser.add_argument("--version", action='store_true', help=f"Current ${_package_name} version")

    # Return parser
    return parser
