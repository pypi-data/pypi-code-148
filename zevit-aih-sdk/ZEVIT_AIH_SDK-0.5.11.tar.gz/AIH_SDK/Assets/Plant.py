from AIH_SDK.Assets.AssetsObject import AssetsObject


class Plant(AssetsObject):
    
    def __init__(self, api_version='1.4'):
        super().__init__()
        self._endpoint = 'plants'
        self._version = api_version
    
    
