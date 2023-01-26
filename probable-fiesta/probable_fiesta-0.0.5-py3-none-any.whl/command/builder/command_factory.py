"""Command Factory class."""
from .command import Command

class CommandFactory:
    @staticmethod
    def new_command(name, function, args):
        return Command(name, function, args)