from AIH_SDK.DataProcessing.DataProcessingObject import DataProcessingObject


class Job(DataProcessingObject):
    
    def __init__(self, api_version='1.2'):
        super().__init__()
        self._endpoint = 'Jobs'
        self._version = api_version