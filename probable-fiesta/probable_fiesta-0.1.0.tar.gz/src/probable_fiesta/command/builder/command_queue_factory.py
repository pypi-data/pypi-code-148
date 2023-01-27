from .command_queue import CommandQueue

class CommandQueueFactory:
    @staticmethod
    def new_command_queue(commands):
        return CommandQueue(commands)
