"""Unit test file for main_app.py."""
from src.probable_fiesta.app import main as main_app
from src.probable_fiesta.app.builder.app import App
from src.probable_fiesta.command.builder import command
from src.probable_fiesta.logger.logging_config import set_logger
from src.probable_fiesta.__about__ import __version__
from src.probable_fiesta.config.variables import PackageDef, VariablesDef

from logging import DEBUG
from unittest import TestCase

# Create a logger if needed for testing cases
LOG_TEST = set_logger("test_main_app", DEBUG)  # Defaults as INFO




class TestMainApp(TestCase):

    def setUp(self):
        self.app = App()

    # Health-check function test - get current version
    def test_function_get_version(self):
        LOG_TEST.info("Test function get_version()")
        # This should never fail :)
        expected = f"{PackageDef.NAME} v.{VariablesDef.VERSION}"
        self.assertEqual(main_app.get_version(), expected)

    def test_create_command_function_version(self):
        c = command.Command().new_with_args("version test", main_app.get_version, None)
        self.app.command = c
        stdout = self.app.invoke()
        #LOG.debug(stdout)
        expected = f"{PackageDef.NAME} v.{VariablesDef.VERSION}" 
        self.assertEqual(stdout, expected)

    def test_argument(self):
        arg = "--version"
        expected = f"{PackageDef.NAME} v.{VariablesDef.VERSION}"
        self.assertEqual(main_app.main([arg]), expected)

    def test_argument_invalid(self):
        arg = "--invalid"
        expected = f"unrecognized arguments: {arg}"
        self.assertEqual(main_app.main([arg]), expected)
