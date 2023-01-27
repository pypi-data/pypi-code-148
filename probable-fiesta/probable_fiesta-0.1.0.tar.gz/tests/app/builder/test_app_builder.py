"""Unit test file for app.builder.app_builder.py."""
from src.probable_fiesta.app.builder import app_builder
from src.probable_fiesta.app.builder import context
from src.probable_fiesta.logger.logging_config import set_logger
from src.probable_fiesta.command.builder.command_factory import CommandFactory
from src.probable_fiesta.command.builder.command_queue import CommandQueue

# Create a logger
from logging import DEBUG
from unittest import TestCase
LOG = set_logger("test_app_builder", DEBUG)


class TestAppBuilderMyAppBuilder(TestCase):

    def setUp(self):
        self.aB = app_builder.AppBuilder()

    def test_init(self):
        LOG.info("Test init")

        self.aB = app_builder.AppBuilder()
        app = self.aB\
            .name\
                .set_name("app_name")\
            .arguments\
                .set_arguments(["--test-app", "test_argument"])\
            .args_parser\
                .add_argument("--test-app", type=str, help="test app builder")\
            .context\
                .add_context(context.Context.Factory().new_context(
                    "test_app",
                    CommandQueue.new([
                        [CommandFactory.new_command("test_app_func", lambda x: x, "repeated")]
                    ])))\
            .validate()\
            .build()
        print(app)
        self.assertEqual(app.name, "app_name")