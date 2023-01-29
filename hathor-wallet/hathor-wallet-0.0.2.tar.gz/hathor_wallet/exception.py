

class HathorWalletError(Exception):
    '''Error class to handle errors when calling methods'''
    def __init__(self, message: str) -> None:
        self.message = message
