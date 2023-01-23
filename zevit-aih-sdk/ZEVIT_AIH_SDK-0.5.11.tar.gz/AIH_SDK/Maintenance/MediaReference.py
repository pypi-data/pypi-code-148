from AIH_SDK.Maintenance.MaintenanceObject import MaintenanceObject


class MediaReference(MaintenanceObject):
    
    def __init__(self, api_version='1.0'):
        super().__init__()
        self._endpoint = 'MediaReferences'
        self._version = api_version