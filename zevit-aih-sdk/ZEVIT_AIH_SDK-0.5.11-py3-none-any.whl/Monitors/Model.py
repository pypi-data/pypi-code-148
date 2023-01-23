from AIH_SDK.Monitors.MonitorsObject import MonitorsObject


class Model(MonitorsObject):
    
    def __init__(self, api_version='1.0'):
        super().__init__()
        self._endpoint = 'Models'
        self._version = api_version