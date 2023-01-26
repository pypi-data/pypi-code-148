"""Test file for cli/v1.py."""
from logging import DEBUG
from unittest import TestCase

from src.probable_fiesta.cli.v1 import create_argument_parser
from src.probable_fiesta.logger.logging_config import set_logger

LOG = set_logger("test_v1", DEBUG)  # Create a logger if needed. Default: INFO


class TestCliV1(TestCase):

    # setup
    def setUp(self):
        self.parser = create_argument_parser()

    def test_parse_arguments_short_flags(self):
        """Test parsed arguments."""
        # you can also test long flags but it's redundant.
        parsed = self.parser.parse_args(['--version'])
        self.assertEqual(parsed.version, True)
        ## Add more tests here

    def test_parse_arguments_invalid(self):
        test_arguments = '--unknown invalid'
        self.parser.parse_args(test_arguments.split())
        expected = f"unrecognized arguments: {test_arguments}"
        self.assertEqual(self.parser.error_message, expected)

    def test_parse_arguments_empty(self):
        test_arguments = None
        self.parser.parse_args(test_arguments)
        print(self.parser.error_message)
        expected = "invalid empty arguments"
        self.assertEqual(self.parser.error_message, expected)