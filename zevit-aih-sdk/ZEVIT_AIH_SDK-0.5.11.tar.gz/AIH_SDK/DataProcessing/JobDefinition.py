from AIH_SDK.DataProcessing.DataProcessingObject import DataProcessingObject

class JobDefinition(DataProcessingObject):
    
    def __init__(self, api_version='1.2'):
        super().__init__()
        self._endpoint = 'JobDefinitions'
        self._version = api_version