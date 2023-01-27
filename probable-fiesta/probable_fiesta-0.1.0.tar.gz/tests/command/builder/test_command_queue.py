"""Unit test file for command.builder.command_queue.py."""
from src.probable_fiesta.command.builder import command_queue
from src.probable_fiesta.logger.logging_config import set_logger

from logging import DEBUG
from unittest import TestCase

# Create a logger
LOG = set_logger("test_command_queue", DEBUG)


class TestCommandBuilderCommandQueue(TestCase):

    def setUp(self):
        self.command_queue = command_queue.CommandQueue()

    def test_init(self):
        LOG.info("Test init")
        self.command_queue = command_queue.CommandQueue()
        self.assertEqual(self.command_queue.queue, [])

    def test_add_new_command(self):
        LOG.info("Test add new command")
        function = lambda: "Hello World!"
        self.command_queue = command_queue.CommandQueue()
        self.command_queue.add_new_command("test", function, "--version")
        # test _str__
        LOG.debug(str(self.command_queue))
        exp = "CommandQueue: loaded commands: 1 executed commands: [] "
        self.assertEqual(str(self.command_queue), exp)
    
    def test_show(self):
        LOG.info("Test show")
        function = lambda: "Hello World!"
        self.command_queue = command_queue.CommandQueue()
        self.command_queue.add_new_command("test", function, "--version")
        # test _str__
        queue = self.command_queue.show()
        for command in queue:
            print(command)
        LOG.debug(str(queue))
        self.assertEqual(len(queue), 1)

    def test_run_all(self):
        LOG.info("Test run all")
        args = "--version"
        function = lambda x: (args)
        self.command_queue = command_queue.CommandQueue()
        self.command_queue.add_new_command("test1", function, args)
        self.command_queue.add_new_command("test2", function, args)
        self.command_queue.run_all()
        self.assertEqual(str(self.command_queue), "CommandQueue: loaded commands: 0 executed commands: ['--version', '--version'] ")

    def test_get_history(self):
        LOG.info("Test get history")
        function = lambda x: (x)
        self.command_queue = command_queue.CommandQueue()
        self.command_queue.add_new_command("test1", function, "--test1")
        self.command_queue.add_new_command("test2", function, "--test2")
        self.command_queue.run_all()
        history = self.command_queue.get_history()
        self.assertEqual(history, ["--test1", "--test2"])