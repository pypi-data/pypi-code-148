from AIH_SDK.Assets.AssetsObject import AssetsObject


class Equipment(AssetsObject):
    
    def __init__(self, api_version='1.4'):
        super().__init__()
        self._endpoint = 'equipment'
        self._version = api_version

        
