from AIH_SDK.Signals.SignalsObject import SignalsObject


class Category(SignalsObject):
    
    def __init__(self, api_version='1.2'):
        super().__init__()
        self._endpoint = 'Categories'
        self._version = api_version