"""Unit test file for logger.builder.logger.py."""
from src.probable_fiesta.logger.builder import logger

from unittest import TestCase

import os
ROOT_DIR = str(os.path.dirname(os.path.abspath(__file__)).rsplit("/tests")[0])

class TestLogger(TestCase):

    def setUp(self):
        self.logger = None

    def test_init(self):
        print("Test init")
        self.logger = logger.Logger()

        self.assertEqual(self.logger.name, None)
        self.assertEqual(self.logger.level, None)
        self.assertEqual(self.logger.fmt, None)
        self.assertEqual(self.logger.directory, None)
        self.assertEqual(self.logger.logger, None)
        self.assertEqual(self.logger.file_handler, None)

        # test _str__
        self.assertEqual(str(self.logger), "Logger: {'name': None, 'level': None, 'fmt': None, 'directory': None, 'logger': None, 'file_handler': None}")

    def test_new(self):
        print("Test new")
        log_name = "test_logger"
        log_level = "DEBUG"
        log_fmt = 'simple'
        log_directory = ROOT_DIR+'/tests/logs'

        self.logger = logger.Logger().new(log_name, log_level, log_fmt, log_directory)

        self.assertEqual(self.logger.name, log_name)
        self.assertEqual(self.logger.level, log_level)
        self.assertEqual(self.logger.fmt, log_fmt)
        self.assertEqual(self.logger.directory, log_directory)
        self.assertEqual(self.logger.logger, None)
        self.assertEqual(self.logger.file_handler, None)

    def test_set_logger(self):
        print("Test set_logger")
        self.logger = logger.Logger()
        self.logger.set_logger("MY_MOCK_CLASS")
        self.assertEqual(self.logger.logger, "MY_MOCK_CLASS")

    def test_get_logger(self):
        print("Test get_logger")
        log_name = "test_logger"
        log_level = "DEBUG"
        log_fmt = 'simple'
        log_directory = ROOT_DIR+'/tests/logs'
        self.logger = logger.Logger().new(log_name, log_level, log_fmt, log_directory)
        parsed_logger = self.logger.get_logger()
        self.assertEqual(str(parsed_logger.__class__), "<class 'logging.RootLogger'>")

    def test_new_logger(self):
        print("Test new_logger")
        log_name = "test_logger"
        log_level = "DEBUG"
        log_fmt = 'simple'
        log_directory = ROOT_DIR+'/tests/logs'
        self.logger = logger.Logger().new_logger(log_name, log_level, log_fmt, log_directory)
        self.assertEqual(str(self.logger.__class__), "<class 'logging.RootLogger'>")

    def test_factory_new(self):
        print("Test factory new")
        log_name = "test_logger"
        log_level = "DEBUG"
        log_fmt = 'simple'
        log_directory = ROOT_DIR+'/tests/logs'
        self.logger = logger.Logger().Factory.new(log_name, log_level, log_fmt, log_directory)
        self.assertEqual(str(self.logger.name), "test_logger")

    def test_factory_create_file_handler(self):
        print("Test factory create_file_handler")
        log_name = "test_logger"
        log_level = "DEBUG"
        log_fmt = 'simple'
        log_directory = ROOT_DIR+'/tests/logs'
        self.logger = logger.Logger().Factory.new(log_name, log_level, log_fmt, log_directory)
        file_handler = self.logger.create_file_handler()
        factory_file_handler = logger.Logger().Factory.create_file_handler(log_name, log_level, log_fmt, log_directory)
        self.assertEqual(file_handler.name, factory_file_handler.name)