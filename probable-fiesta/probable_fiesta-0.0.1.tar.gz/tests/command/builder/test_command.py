"""Unit test file for command.builder.command.py."""
from src.probable_fiesta.command.builder import command
from src.probable_fiesta.logger.logging_config import set_logger

from logging import DEBUG
from unittest import TestCase

# Create a logger
LOG = set_logger("test_command", DEBUG)


class TestCommandBuilderCommand(TestCase):

    def setUp(self):
        self.command = command.Command()

    def test_init(self):
        LOG.info("Test init")
        self.command = command.Command()
        self.assertEqual(self.command.name, None)
        self.assertEqual(self.command.function, None)
        self.assertEqual(self.command.args, None)
        # test _str__
        LOG.debug(str(self.command))
        self.assertEqual(str(self.command), "Command: {'name': None, 'function': None, 'args': None}")

    def test_new(self):
        LOG.info("Test new")
        self.command = command.Command().new()
        self.assertEqual(self.command.name, None)
        self.assertEqual(self.command.function, None)
        self.assertEqual(self.command.args, None)
        # test _str__
        LOG.debug(str(self.command))
        self.assertEqual(str(self.command), "Command: {'name': None, 'function': None, 'args': None}")

    def test_new_with_args(self):
        LOG.info("Test new with args")
        function = lambda: "Hello World!"
        self.command = command.Command().new_with_args("test", function, "--version")
        self.assertEqual(self.command.name, "test")
        self.assertAlmostEqual(self.command.function, function)
        self.assertEqual(self.command.args, "--version")
        # test _str__
        LOG.debug(str(self.command))
        self.assertEqual(str(self.command), "Command: {'name': 'test', "+f"'function': {function},"+" 'args': '--version'}")

    def test_factory(self):
        LOG.info("Test factory")
        function = lambda: "Hello World!"
        self.command = command.Command().Factory.new_command("test", function, "--version")
        self.assertEqual(self.command.name, "test")
        self.assertEqual(self.command.function, function)
        self.assertEqual(self.command.args, "--version")
        # test _str__
        LOG.debug(str(self.command))
        self.assertEqual(str(self.command), "Command: {'name': 'test', "+f"'function': {function},"+" 'args': '--version'}")

    def test_invoke(self):
        LOG.info("Test invoke")
        self.command = command.Command().new_with_args("test", lambda: "Hello World!", None)
        stdout = self.command.invoke()
        print(stdout)
        LOG.debug(stdout)
        self.assertEqual(stdout, "Hello World!")

    def test_invoke_with_args(self):
        LOG.info("Test invoke with args")
        self.command = command.Command()
        self.command.function = lambda x: (self.command.args)
        self.command.args = "--version"
        stdout = self.command.invoke()
        LOG.debug(stdout)
        self.assertEqual(stdout, self.command.args)

    def test_invoke_without_function(self):
        LOG.info("Test invoke without function expect error log")
        self.command = command.Command()
        stdout = self.command.invoke()
        LOG.debug(stdout)
        self.assertEqual(stdout, None)

