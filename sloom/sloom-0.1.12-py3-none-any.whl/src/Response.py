from .Core.Terminal import *
from .ResponseType import *

class Response(ResponseType):
    def __init__(self, response, url) -> None:
        self.response = response
        self.url = url
        self.debug_init()
    
    def debug_init(self):
        Terminal.put(f"{self.url} - {bcolors.OKGREEN}success{bcolors.ENDC}")
