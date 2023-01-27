"""Context Factory class."""
from .context import Context

class ContextFactory:
    @staticmethod
    def new_context(name=None, command_queue=None):
        return Context(name, command_queue)