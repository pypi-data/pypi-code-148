from AIH_SDK.Signals.SignalsObject import SignalsObject

class DataOrigin(SignalsObject):
    
    def __init__(self, api_version='1.2'):
        super().__init__()
        self._endpoint = 'DataOrigins'
        self._version = api_version