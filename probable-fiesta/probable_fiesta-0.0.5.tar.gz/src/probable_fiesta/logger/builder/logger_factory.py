from .logger import Logger
from ...config.variables import LoggerDef

class LoggerFactory:
    @staticmethod
    def new_logger(name=None, level=None, fmt=None, directory=None):
        return Logger.new(name, level, fmt, directory)

    @staticmethod
    def new_logger_default(name=None, level=None, fmt=None, directory=None):
        directory = directory
        if not directory:
            directory = LoggerDef.ROOT_DIR+'/logger'
        if not fmt:
            fmt = LoggerDef.FORMAT
        return Logger.new(name, level, fmt, directory) 

    @staticmethod
    def new_logger_flask(app, name, level, fmt, directory):
        file_handler = Logger.Factory.create_file_handler(name, level, fmt, directory)
        app.logger.addHandler(file_handler)
        return app.logger