import logging
from logging.handlers import RotatingFileHandler

class Logger:
    def __init__(self, name=None, level=None, fmt='simple', directory=None):
        self.logger = None
        self.name = name,
        self.level = level
        self.fmt = fmt
        self.directory = directory
        self.file_handler = None

    def __str__(self):
        return f"Logger: {self.__dict__}"

    def set_logger(self, logger): 
        self.logger = logger

    def set_file_handler(self, file_handler):
        self.file_handler = file_handler

    def get_file_handler(self):
        return self.file_handler

    def prepare_file_handler(self):
        _formatter = self.set_formatter_format(self.fmt)
        _log_path = f"{self.directory}/{self.name}.log"
        print(f"Building logger {self.name} at path: {_log_path}")
        _file_h = logging.FileHandler(_log_path, 'a')
        _file_h.setFormatter(_formatter)
        self.file_handler = _file_h
        return self.file_handler

    def set_logger_with_vars(self, name=None, level=None, fmt='simple', directory=None):
        self.name = name
        self.level = level
        self.fmt = fmt
        self.directory = directory
        return self

    def create_logger(self, name=None, level=None, fmt='simple', directory=None):
        self.set_logger_with_vars(name, level, fmt, directory)
        self.prepare_file_handler()
        _logger = logging.getLogger(self.name)
        _logger.setLevel(self.level)
        _logger.addHandler(self.file_handler)
        self.set_logger(_logger)
        return self.logger

    def build_logger(self):
        self.logger = self.create_logger(self.name, self.level, self.fmt, self.directory)
        return self.logger

    def get_logger(self):
        return self.logger

    def get_logger_by_name(self, name):
        return logging.getLogger(name)

    def set_formatter_format(option):
        """Choose a formatter from the following or create your own.
        `simple` - Time LoggerName Level - Message
        `process` - Time moduleName -> processId lineNo Level - Message
        `function` - Time moduleName funcName -> lineNo Level - Message
        :param options: simple, process, function, custom.
        :return: formatter to be set with `setFormatter`.
        """
        # Check for valid input
        options = ['simple', 'process', 'function']
        if option not in options:
            print("Log formatter input error. Only supported: ", options)
            raise ValueError
        # Define a simple formatter
        if option == 'simple':
            return logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # Define a process formatter
        if option == 'process':
            return logging.Formatter(
                '%(asctime)s %(module)s -> %(process)d %(lineno)d %(levelname)s' +
                ' -  %(message)s')
        # Define a function formatter
        if option == 'function':
            return logging.Formatter(
                '%(asctime)s %(module)s %(funcName)s -> %(lineno)d %(levelname)s' +
                ' -  %(message)s')

#application.logger.addHandler(YourFileHandler)

    class Factory:
        @staticmethod
        def new_logger():
            return Logger()

        @staticmethod
        def new_logger_default(name=None):
            return Logger().create_logger_with_vars(name, logging.INFO, 'simple', 'logs')

        @staticmethod
        def new_logger_flask_handler(self, name=__name__, level=logging.DEBUG, fmt='simple', directory='/logs'):
            self.logger = logging.getLogger(name)
            self.fmt = self.set_formatter_format(fmt)
            self.level = level
            self.directory = directory
            self.file_handler = RotatingFileHandler(f'{self.directory}/{self.name}.log', maxBytes=1024,backupCount=5)
            #self.handler = RotatingFileHandler('/opt/python/log/application.log', maxBytes=1024,backupCount=5)
            self.file_handler.setFormatter(self.fmt)
            return self.file_handler

    factory = Factory()

#class LoggerFlask(Logger):
    #logger = logging.getLogger(__name__)
    #formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    #logger.setLevel(logging.DEBUG)
    ##handler = RotatingFileHandler('/home/vagrant/opt/python/log/application.log', maxBytes=1024,backupCount=5)
    #handler = RotatingFileHandler('/opt/python/log/application.log', maxBytes=1024,backupCount=5)
    ##handler = RotatingFileHandler('/var/log/application.log', maxBytes=1024,backupCount=5)
    #handler.setFormatter(formatter)

    #application = Flask(__name__)
    #login_manager = LoginManager()
    #login_manager.init_app(application)
    #application.logger.addHandler(handler)