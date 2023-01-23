from AIH_SDK.Monitors.MonitorsObject import MonitorsObject


class PropertyDefinition(MonitorsObject):
    
    def __init__(self, api_version='1.0'):
        super().__init__()
        self._endpoint = 'PropertyDefinitions'
        self._version = api_version