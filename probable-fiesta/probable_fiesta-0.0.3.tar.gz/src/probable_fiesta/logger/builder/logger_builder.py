from .logger import Logger

class LoggerBuilder:
    def __init__(self, logger=None):
        if logger is None:
            self.logger = Logger().new()
        else:
            self.logger = logger().new().set_logger(logger)

    def __str__(self):
        return f"LoggerBuilder: {self.__dict__}"

    @property
    def logger(self):
        return LoggerBuilderLogger(self.logger)

    def build(self):
        return self.logger

class LoggerBuilderLogger(LoggerBuilder):
    def __init__(self, logger):
        super().__init__(logger)

    def get_logger_flask_application(self, application, name=None, level=None, fmt=None, directory=None, filename=None):
        _file_handler = self.logger.Factory.new_logger_handler(name, level, fmt, directory, filename)
        if not self.logger.file_handler:
            print("File handler not set")
        application.logger.add_handler = self.logger.file_handler
        yield application

    def get_logger_default(self, name=None, level=None, fmt=None, directory=None, filename=None):
        print("Getting default logger")
        self.logger = self.logger.Factory.new_logger(name, level, fmt, directory, filename)
        return self