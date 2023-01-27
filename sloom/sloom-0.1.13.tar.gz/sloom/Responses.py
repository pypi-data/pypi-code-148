from .Response import *
from .RequestError import *
from .Core.List import *
from .ResponseType import *

class Responses(List):
    def __init__(self) -> None:
        List.__init__(self, ResponseType)

    def removeErrors(self):
        """
        Use to filter a list to only have responses without errors
        """
        self.filter(self._removeErrors)
    
    def _removeErrors(self, response):
        return isinstance(response, Response)