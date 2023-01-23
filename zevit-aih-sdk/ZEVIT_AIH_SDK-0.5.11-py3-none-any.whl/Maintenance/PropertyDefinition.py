from AIH_SDK.Maintenance.MaintenanceObject import MaintenanceObject


class PropertyDefinition(MaintenanceObject):
    
    def __init__(self, api_version='1.0'):
        super().__init__()
        self._endpoint = 'PropertyDefinitions'
        self._version = api_version