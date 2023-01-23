from AIH_SDK.Designations.DesignationsObject import DesignationsObject


class PropertyDefinition(DesignationsObject):
    
    def __init__(self, api_version='1.1'):
        super().__init__()
        self._endpoint = 'PropertyDefinitions'
        self._version = api_version