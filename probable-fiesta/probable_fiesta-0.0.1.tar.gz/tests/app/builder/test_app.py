"""Unit test file for app.builder.app.py."""
from src.probable_fiesta.app.builder import app
from src.probable_fiesta.command.builder import command
from src.probable_fiesta.logger.logging_config import set_logger

from logging import DEBUG
from unittest import TestCase

# Create a logger
LOG = set_logger("test_app", DEBUG)


class TestAppBuilderApp(TestCase):

    def setUp(self):
        self.app = app.App()

    #def test_init(self):
        #expected = "App: {'name': None, 'args': None, 'argument_parser': None, 'validated_args': None, 'config': None, 'variables': None, 'error': None, 'command': None, 'command_list': None, 'command_list_builder': None}"
        #self.assertEqual(str(self.app), expected)

    def test_invoke_manual(self):
        LOG.info("Test invoke")

        c = command.Command().new_with_args("test", lambda: "Hello World!", None)
        self.app.command = c
        stdout = self.app.command.invoke()
        LOG.debug(stdout)
        self.assertEqual(stdout, "Hello World!")

    def test_invoke(self):
        LOG.info("Test invoke")

        c = command.Command().new_with_args("test", lambda: "Hello World!", None)
        self.app.command = c
        stdout = self.app.invoke()
        LOG.debug(stdout)
        self.assertEqual(stdout, "Hello World!")