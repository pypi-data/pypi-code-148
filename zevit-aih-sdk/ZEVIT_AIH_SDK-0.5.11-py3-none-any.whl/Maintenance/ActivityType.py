from AIH_SDK.Maintenance.MaintenanceObject import MaintenanceObject


class ActivityType(MaintenanceObject):
    
    def __init__(self, api_version='1.0'):
        super().__init__()
        self._endpoint = 'ActivityTypes'
        self._version = api_version