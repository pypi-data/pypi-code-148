"""Unit test file for app.builder.my_app_builder.py."""
from src.probable_fiesta.app.builder import my_app_builder
from src.probable_fiesta.app.builder import context_factory
from src.probable_fiesta.cli.v1 import create_argument_parser
from src.probable_fiesta.logger.logging_config import set_logger

from logging import DEBUG
from unittest import TestCase

# Create a logger
LOG = set_logger("test_my_app_builder", DEBUG)


class TestAppBuilderMyAppBuilder(TestCase):

    def setUp(self):
        self.my_app_builder = my_app_builder.MyAppBuilder()

    def test_init(self):
        LOG.info("Test init")
        self.my_app_builder = my_app_builder.MyAppBuilder()
        my_app = self.my_app_builder.name.set_name("test").build()
        self.assertEqual(my_app.name, "test")

    def test_my_app_builder_name(self):
        LOG.info("Test MyAppBuilder name")

        self.my_app_builder = my_app_builder.MyAppBuilder()
        my_app = self.my_app_builder.name.set_name("test").build()
        self.assertEqual(my_app.name, "test")

    def test_my_app_builder_context(self):
        LOG.info("Test MyAppBuilder context")

        # create context
        context = context_factory.ContextFactory.new_context("test")

        self.my_app_builder = my_app_builder.MyAppBuilder()
        my_app = self.my_app_builder.context.set_context(context).build()
        self.assertEqual(my_app.context.name, "test")

    def test_my_app_builder_args(self):
        LOG.info("Test MyAppBuilder args")
        args = ["--version"]

        # Validate args
        parser = create_argument_parser()
        args = parser.parse_args(args)
        if parser.error_message:
            stdout = f"{parser.error_message}"
        if not args:
            stdout = f"no args."
        self.assertEqual(args.version, True)
