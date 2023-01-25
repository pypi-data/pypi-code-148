"""Command class."""
from ...logger.logger_module import get_logger

#from logging import ERROR

# Create a logger
#LOG = set_logger("command", ERROR)
LOG = get_logger(name='command', level='error')

class Command:

    def __init__(self, name=None, function=None, args=None):
        self.name = name
        self.function = function
        self.args = args

    def __str__(self):
        return f"Command: {self.__dict__}"

    def invoke(self):
        if self.function is not None and self.args is not None:
            return self.function(self.args)
        elif self.function is not None and self.args is None:
            return self.function()
        else:
            LOG.error("Missing self.function")
            return None

    @staticmethod
    def new():
        return Command(None, None, None)

    @staticmethod
    def new_with_args(name, function, args):
        return Command(name, function, args)

    class Factory():
        @staticmethod
        def new_command(name, function, args):
            if function is None:
                LOG.error("Missing function")
                return None
            return Command(name, function, args)
    
    factory = Factory()
