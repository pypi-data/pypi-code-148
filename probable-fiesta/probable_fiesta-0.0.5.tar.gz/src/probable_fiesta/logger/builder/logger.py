"""Logger class."""
import logging

class Logger:

    def __init__(self, name=None, level=None, fmt=None, directory=None):
        self.name = name
        self.level = level
        self.fmt = fmt
        self.directory = directory
        self.logger = None 
        self.file_handler = None

    def __str__(self) -> str:
        return f"Logger: {self.__dict__}"

    def get_logger(self, name=None, level=None, fmt=None, directory=None):
        self.name = name
        self.level = level
        self.fmt = fmt
        self.directory = directory
        if self.name is None:
            print("Name not set. Cannot create logger.")
            return None
        _logger = logging.getLogger(self.name)
        _logger.setLevel(self.parse_level(self.level))
        if self.file_handler is None:
            self.create_file_handler()

        _logger.addHandler(self.file_handler)
        self.logger = _logger
        return self.logger

    def create_file_handler(self):
        if self.name is None:
            print("Name not set. Cannot create file handler.")
            return None
        if not self.directory:
            self.directory = "./"
        _file_handler = logging.FileHandler(self.directory+f"/{self.name}.log")
        _file_handler.setLevel(self.parse_level(self.level))
        _file_handler.setFormatter(self.fmt)
        self.file_handler = _file_handler
        print("File handler created", self.file_handler)
        return self.file_handler

    def parse_level(self, level):  # defaults to info
        if level is None:
            return logging.INFO
        if level == "DEBUG":
            return logging.DEBUG
        if level == "INFO":
            return logging.INFO
        if level == "WARNING":
            return logging.WARNING
        if level == "ERROR":
            return logging.ERROR
        if level == "CRITICAL":
            return logging.CRITICAL
        return logging.INFO

    def set_logger(self, logger):
        self.logger = logger
        return self.logger

    @staticmethod
    def new(name=None, level=None, fmt=None, directory=None):
        return Logger(name, level, fmt, directory)

    @staticmethod
    def new_logger(name=None, level=None, fmt=None, directory=None):
        logger = Logger.new(name, level, fmt, directory)
        return logger.get_logger()


    class Factory():
        @staticmethod
        def new(name=None, level=None, fmt=None, directory=None):
            return Logger.new(name, level, fmt, directory)

        @staticmethod
        def create_file_handler(name=None, level=None, fmt=None, directory=None) -> logging.FileHandler:
            logger = Logger.new(name, level, fmt, directory)
            return logger.create_file_handler()


    factory = Factory()



