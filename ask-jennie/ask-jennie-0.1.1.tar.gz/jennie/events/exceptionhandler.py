import requests, json
from .colorprinting import ColorPrinting

logger = ColorPrinting()

class ExceptionHanlder():
    '''
    The class is responsible for handling error
    '''
    def __init__(self, token):
        self.headers = {
            "Content-type": "application/json",
            "token": token,
        }

    def log_error(self, log_info):
        if self.headers["token"]:
            resp = requests.post(
                url="https://api.ask-jennie.com/v1/log/exception/",
                headers=self.headers,
                json=log_info
            )

    def handle_error(self, exception, traceback, commands):
        '''
        Get traces of exception, upload it to
        Jennie Exception Logger.
        :return: Error logged.
        '''
        self.log_error(
            {
                "message": str(exception),
                "exception": str(traceback),
                "commands": json.dumps(commands)
            }
        )
        logger.error(str(exception))
        return exception