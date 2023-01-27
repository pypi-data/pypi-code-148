"""Context holder class."""
from .context import Context

class ContextHolder:
    def __init__(self, context_holder={}):
        self.context_holder = context_holder
    
    def add_context(self, context):
        if not isinstance(context, Context):
            raise TypeError("Context must be of type Context")
        self.context_holder[context.name] = context
        return self
    
    def validate(self, parsed_args):
        if parsed_args is None:
            print("No parsed args")
            return False
        for name in self.context_holder:
            context = self.context_holder[name]
            if not context.name in parsed_args:
                #print("No validated context: ", context.name)
                return False
        return True