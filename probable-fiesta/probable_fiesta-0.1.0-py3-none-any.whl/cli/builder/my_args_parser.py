"""CLI v1 Argument Parser."""
import argparse

DESCRIPTION = "There's probably a fiesta somewhere."

class MyArgsParser(argparse.ArgumentParser):

    def __init__(self, *args, **kwargs):
        super(MyArgsParser, self).__init__(*args, **kwargs)

        self.parser = None
        self.error_message = ''

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
        return result