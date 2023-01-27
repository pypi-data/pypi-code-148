"""Unit test file for logger.builder.logger_factory.py."""
from src.probable_fiesta.logger.builder import logger_factory

from src.probable_fiesta.config.variables import LoggerDef

from unittest import TestCase

class TestLogger(TestCase):

    def setUp(self):
        self.logger_factory = logger_factory.LoggerFactory()

    def test_new_logger(self):
        print("Test new_logger")
        logger = self.logger_factory.new_logger()

        self.assertEqual(logger.name, None)
        self.assertEqual(logger.level, None)
        self.assertEqual(logger.fmt, None)
        self.assertEqual(logger.directory, None)
        self.assertEqual(logger.logger, None)
        self.assertEqual(logger.file_handler, None)

        # test _str__
        self.assertEqual(str(logger), "Logger: {'name': None, 'level': None, 'fmt': None, 'directory': None, 'logger': None, 'file_handler': None}")

    def test_new_logger_default(self):
        print("Test new_logger_default")
        log_name = "test_logger"
        log_level = LoggerDef.LEVEL
        log_fmt = LoggerDef.FORMAT
        log_directory = LoggerDef.ROOT_DIR+'/logger'

        logger = self.logger_factory.new_logger_default(log_name, log_level, log_fmt, log_directory)

        self.assertEqual(logger.name, log_name)
        self.assertEqual(logger.level, log_level)
        self.assertEqual(logger.fmt, log_fmt)
        self.assertEqual(logger.directory, log_directory)
        self.assertEqual(logger.logger, None)
        self.assertEqual(logger.file_handler, None)
