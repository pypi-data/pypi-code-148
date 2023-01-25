"""Unit test file for command.builder.command_builder.py."""
from src.probable_fiesta.command.builder import command_builder
from src.probable_fiesta.logger.logging_config import set_logger

from logging import DEBUG
from unittest import TestCase

# Create a logger
LOG = set_logger("test_command_builder", DEBUG)


class TestCommandBuilderCommandBuilder(TestCase):

    def setUp(self):
        self.command_builder = command_builder.CommandBuilder()

    def test_init(self):
        LOG.info("Test init")
        cb = command_builder.CommandBuilder()
        self.command_builder = cb
        self.assertEqual(self.command_builder, cb)

    def test_property_queue_add_new_command(self):
        LOG.info("Test property queue add new command")
        self.command_builder = command_builder.CommandBuilder()
        self.command_builder.queue.add_new_command("test", lambda x: ("test"), "test").build()
        # access inner command_queue
        self.assertEqual(self.command_builder.queue.command_queue.length, 1)

    def test_property_queue_add_new_command_chain(self):
        LOG.info("Test property queue add new command chain")
        self.command_builder = command_builder.CommandBuilder()
        self.command_builder.queue\
            .add_new_command("test1", lambda x: ("test"), "test")\
            .add_new_command("test2", lambda x: ("test"), "test")\
            .build()
        # access inner command_queue
        self.assertEqual(self.command_builder.queue.command_queue.length, 2)