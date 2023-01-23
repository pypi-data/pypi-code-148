import io

import AIH_SDK.AIHExceptions as AIHE
from AIH_SDK.Maintenance.MaintenanceObject import MaintenanceObject
from PIL import Image


class Media(MaintenanceObject):
    
    def __init__(self, api_version='1.0'):
        super().__init__()
        self._endpoint = 'Medias'
        self._version = api_version
        self._valid_filetypes = ['image', 'document']
    

    def get(self, id:str=None):
        """
        To get a list of all media or a specific media.
        Result is set as self.value
        """
        
        if id:
            self.value = self._client._get(self._api, f'{self._endpoint}/{id}')
        else:
            self.value = self._client._get(self._api, self._endpoint)
        
        return self
            
    
    def download(self, id, filetype):
        f"""
        To download the image/document with a given id.
        IN: id - The name of the media it should get. If not specified or None, it will use the name of the object if it is a dict. 
        filetype - the type of file to be downloaded. If not specified it will use the continer name of the object. Must  be one of the following {self._valid_filetypes}

        
        OUT: (generator) A generator with the downloaded media as an PIL Image if filetype is 'image'. If filetype is 'document' it will output file content.
        """
        

        content = self._client._download_maintenance_media(id)

        if filetype == 'image':
            file = Image.open(io.BytesIO(content))
        elif filetype == 'document':
            file = content
        else:
            raise AIHE.AIHException(f'filetype was {filetype}, but must be one of the following {self._valid_filetypes}')
        
        yield file
    
        
    
    
    def upload(self, file, name:str, filetype:str, exif:bytes=None):
        f"""
        To post the updates that have been made.
        IN: file     - The that should be uploaded
            name     - The name of the file that should be uploaded. Should contain the file extention
            filetype - The type of the file that should be uploaded. Should be one of the following {self._valid_filetypes}.
            exif     - Exif dictionary that is converted to bytes. Is used to set the metadata.
        """
        
        fileextension = name.split('.')[-1]
        _file = io.BytesIO()
        
        if filetype == 'image':
            if exif:
                file.save(_file, format='jpeg' if fileextension.lower() == 'jpg' else fileextension, exif=exif)
            else:
                file.save(_file, format='jpeg' if fileextension.lower() == 'jpg' else fileextension)

            _file.seek(0)
        elif filetype == 'document':
            _file = file
        else:
            raise AIHE.AIHException(f'filetype was {filetype}, but must be one of the following {self._valid_filetypes}')
        
        response_json = self._client._upload_maintenance_media(_file, name, filetype)
        self.value = response_json
        
        return self
    

    def get_keys(self):
        return ['id', 'name', 'displayName', 'dbStatus', 'type', 'container']
