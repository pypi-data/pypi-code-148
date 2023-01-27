from .Core.Terminal import *
from .ResponseType import *

class RequestError(ResponseType):
    def __init__(self, status_code, url) -> None:
        self.status_code = status_code
        self.url = url
        self.debug_init()
    
    def debug_init(self):
        Terminal.put(f"{self.url} - {bcolors.FAIL}ERROR{bcolors.ENDC}")