from AIH_SDK.Maintenance.MaintenanceObject import MaintenanceObject


class Category(MaintenanceObject):
    
    def __init__(self, api_version='1.0'):
        super().__init__()
        self._endpoint = 'Categories'
        self._version = api_version