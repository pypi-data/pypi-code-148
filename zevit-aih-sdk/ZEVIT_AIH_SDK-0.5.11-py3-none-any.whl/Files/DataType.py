from AIH_SDK.Files.FilesObject import FilesObject


class DataType(FilesObject):
    
    def __init__(self, api_version='1.3'):
        super().__init__()
        self._endpoint = 'DataTypes'
        self._version = api_version