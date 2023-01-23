from AIH_SDK.Identity.IdentityObject import IdentityObject


class User(IdentityObject):
    
    def __init__(self, api_version='1.0'):
        super().__init__()
        self._endpoint = 'Users'
        self._version = api_version
    
