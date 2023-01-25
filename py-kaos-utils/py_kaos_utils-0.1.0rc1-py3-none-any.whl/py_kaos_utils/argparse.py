from dateutil import parser


class ArgParseTypes:
    """
    Contains static methods that can be passed to ``argparse.ArgumentParser().add_argument(type=)``

    Example:
        >>> import argparse
        >>> parser = argparse.ArgumentParser()
        >>> parser.add_argument('datetime', type=ArgParseTypes.datetime)
    """

    @staticmethod
    def datetime(s):
        """
        Return a datetime parsed from a cli argument.
        """
        return parser.parse(s)
