"""Context builder class."""
from .context import Context

class ContextBuilder:

    def __init__(self, context=None):
        self.context = context

    @property
    def queue(self):
        return ContextBuilderQueue(self.context)

    def build(self):
        return self

class ContextBuilderQueue(ContextBuilder):

    def __init__(self, context):
        super().__init__(context)

    def set_name(self, name):
        self.context.name = name
        return self

    def set_command_queue(self, command_queue):
        self.context.command_queue = command_queue
        return self