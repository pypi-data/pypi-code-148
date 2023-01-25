"""Unit test file for command.builder.command_factory.py."""
from src.probable_fiesta.command.builder import command_factory
from src.probable_fiesta.logger.logging_config import set_logger

from logging import DEBUG
from unittest import TestCase

# Create a logger
LOG = set_logger("test_command_factory", DEBUG)


class TestCommandBuilderCommandFactory(TestCase):

    def setUp(self):
        self.command = command_factory.CommandFactory()

    # Class is only a factory no need to test init
    #def test_init(self):
        #LOG.info("Test init")
        #self.command = command_factory.CommandFactory()
        #self.assertEqual(self.command.name, None)
        #self.assertEqual(self.command.function, None)
        #self.assertEqual(self.command.args, None)
        ## test _str__
        #LOG.debug(str(self.command))
        #self.assertEqual(str(self.command), "Command: {'name': None, 'function': None, 'args': None}")

    def test_new_command(self):
        LOG.info("Test new command")
        function = lambda: "Hello World!"
        self.command = command_factory.CommandFactory().new_command("test", function, "--version")
        self.assertEqual(self.command.name, "test")
        self.assertEqual(self.command.function, function)
        self.assertEqual(self.command.args, "--version")
        # test _str__
        LOG.debug(str(self.command))
        self.assertEqual(str(self.command), "Command: {'name': 'test', "+f"'function': {function},"+" 'args': '--version'}")
