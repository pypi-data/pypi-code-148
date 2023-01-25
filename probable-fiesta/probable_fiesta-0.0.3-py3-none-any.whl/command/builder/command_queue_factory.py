from .command_queue import CommandQueue

class CommandQueueFactory:
    @staticmethod
    def new_command_queue_empty():
        return CommandQueue()

    @staticmethod
    def new_command_queue_with_queue(queue):
        return CommandQueue(queue)
