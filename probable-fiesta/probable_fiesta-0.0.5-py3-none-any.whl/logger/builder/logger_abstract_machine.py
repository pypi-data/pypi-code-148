from abc import ABC
from enum import Enum, auto

from .logger_factory import LoggerFactory

class AbstractLogger(ABC):
    def create_logger(self):
        pass

class LoggerDefault(AbstractLogger):
    def create_logger(self):
        pass

class LoggerFlask(AbstractLogger):
    def create_logger(self):
        pass

class LoggerAbstractFactory(ABC):
    def create_logger(self, name, level, fmt, directory):
        pass
    def create_logger(self, app, name, level, fmt, directory):
        pass

class DefaultFactory(LoggerAbstractFactory):
    def create_logger(self, name, level, fmt, directory):
        print("Creating default logger")
        logger = LoggerFactory().new_logger(name, level, fmt, directory)
        return logger

class FlaskFactory(LoggerAbstractFactory):
    def create_logger(self, app, name, level, fmt, directory):
        print("Creating flask logger")
        logger = LoggerFactory().new_logger_flask(app, name, level, fmt, directory)
        return logger

class LoggerMachine:
    class Available(Enum):
        DEFAULT = auto()
        FLASK = auto()
    
    factories = []
    initialized = False

    def __init__(self):
        if not self.initialized:
            self.initialized = True
            for d in self.Available:
                name = d.name[0] +  d.name[1:].lower()
                factory_name = name + "Factory"
                factory_instance = eval(factory_name)()
                self.factories.append((name, factory_instance))

    def __str__(self):
        return f"LoggerMachine: Available loggers: {self.factories}"

    def prepare_logger(self):
        print("Available apps:")
        for f in self.factories:
            print(f[0])
        s = input(f'Please pick app (0-{len(self.factories)-1}):')
        idx = int(s)
        return self.factories[idx][1].get()

    def make_logger(self, type, app=None, name=None, level=None, fmt=None, directory=None):
        if type == 'default':
            return DefaultFactory().create_logger(name, level, fmt, directory)
        elif type == 'flask':
            return FlaskFactory().create_logger(app, name, level, fmt, directory)
        else:
            print("Invalid logger type")
            return None

def make_logger(type, app=None, name=None, level=None, fmt=None, directory=None):
    if type == 'default':
        return DefaultFactory().create_logger(name, level, fmt, directory)
    elif type == 'flask':
        return FlaskFactory().create_logger(app, name, level, fmt, directory)
    else:
        print("Invalid logger type")
        return None
