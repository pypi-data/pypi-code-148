from AIH_SDK.Monitors.MonitorsObject import MonitorsObject


class Category(MonitorsObject):
    
    def __init__(self, api_version='1.0'):
        super().__init__()
        self._endpoint = 'Categories'
        self._version = api_version