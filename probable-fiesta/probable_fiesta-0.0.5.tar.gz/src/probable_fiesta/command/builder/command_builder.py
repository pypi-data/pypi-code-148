"""CommandBuilder class."""

from .command_queue import CommandQueue

class CommandBuilder:

    def __init__(self, command_queue=None):
        if command_queue is not None:
            self.command_queue = command_queue
        else:
            self.command_queue = CommandQueue()

    @property
    def queue(self):
        return CommandBuilderQueue(self.command_queue)

    def build(self):
        return self.command_queue

class CommandBuilderQueue(CommandBuilder):

    def __init__(self, command_queue):
        super().__init__(command_queue)

    def add_new_command(self, name, function, args=None):
        self.command_queue.add_new_command(name, function, args)
        return self

    def add_command(self, command):
        self.command_queue.add_command(command)
        return self

    def add_commands(self, commands):
        self.command_queue.add_commands(commands)
        return self

    def add_command_queue(self, command_queue):
        self.command_queue.add_command_queue(command_queue)
        return self

    def add_command_queues(self, command_queues):
        self.command_queue.add_command_queues(command_queues)
        return self

    def add_command_builder(self, command_builder):
        self.command_queue.add_command_queue(command_builder.build())
        return self

    def add_command_builders(self, command_builders):
        for command_builder in command_builders:
            self.add_command_builder(command_builder)
        return self

    def add_command_list(self, command_list):
        self.command_queue.add_command_list(command_list)
        return self

    def add_command_lists(self, command_lists):
        self.command_queue.add_command_lists(command_lists)
        return self

    def add_command_list_builder(self, command_list_builder):
        self.command_queue.add_command_list(command_list_builder.build())
        return self

    def add_command_list_builders(self, command_list_builders):
        for command_list_builder in command_list_builders:
            self.add_command_list_builder(command_list_builder)
        return self

    def add_command_queue_factory(self, command_queue_factory):
        self.command_queue.add_command_queue(command_queue_factory.build())
        return self

    def add_command_queue_factories(self, command_queue_factories):
        for command_queue_factory in command_queue_factories:
            self.add_command_queue_factory(command_queue_factory)
        return self

    def add_command_list_factory(self, command_list_factory):
        self.command_queue.add_command_list(command_list_factory.build())
        return self

    def add_command_list_factories(self, command_list_factories):
        for command_list_factory in command_list_factories:
            self.add_command_list_factory(command_list_factory)
        return self

    def add_command_factory(self, command_factory):
        self.command_queue.add_command(command_factory.build())
        return self

    def add_command_factories(self, command_factories):
        for command_factory in command_factories:
            self.add_command_factory(command_factory)
        return self

    def add_command_builder_factory(self, command_builder_factory):
        self.command_queue.add_command_queue(command_builder_factory.build())
        return self