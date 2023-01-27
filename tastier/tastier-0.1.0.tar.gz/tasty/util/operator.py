class PipeOperator:
    def __init__(self, argument = None):
        self.argument = argument

    def __ror__(self, argument):
        return PipeOperator(argument)

    def __or__(self, function):
        return function(self.argument)


pipe = PipeOperator()
