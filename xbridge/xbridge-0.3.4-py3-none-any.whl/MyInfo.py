


import base64
import json
from mimetypes import MimeTypes
import mimetypes
import os


class MyInfo:
    version: str
    name: str
    avatar_path: str

    def __init__(self, file_path: str):
        try:
            with open(file_path, 'rb') as file:
                    string = file.read().decode(encoding='utf8', errors='strict')
                    obj = json.loads(string)
                    self.version = obj.get("version", "1")
                    self.name = obj.get("name", "unknown")
                    self.avatar_path = os.path.join(os.path.dirname(file_path), obj['avatar'])
                    
        except Exception as e:
            print("Parse MyInfo Error:", e)
            raise Exception("my info is invalid!")


    @property
    def avatar_url(self):
        mime = MimeTypes()
        head_img = ''
        mime_type = mime.guess_type(self.avatar_path)[0] #3 returns a tuple
        if mime_type is None:
            mime_type = "image/png"
        print("mime_type:", mime_type)
        with open(self.avatar_path, 'rb') as f:
            data = base64.b64encode(f.read())
            b64 = data.decode('utf8')
            # print("data:", data)
            # data = .encode('base64')
            head_img = 'data:' + mime_type + ';base64,' + b64
        return head_img








