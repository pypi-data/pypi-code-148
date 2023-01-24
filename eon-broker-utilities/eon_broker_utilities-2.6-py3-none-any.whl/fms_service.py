from dataclasses import replace
import os
from time import time
from typing import Any
import requests
import json
from clint.textui import progress
import requests
import shutil
from tqdm.auto import tqdm

class ManageFiles():
    def __init__(self, fms_config_variables):
        self.fms_host = fms_config_variables['FMS_HOST']
        self.fms_port = fms_config_variables['FMS_PORT'] 
        self.fms_url  = f"{self.fms_host}:{self.fms_port}"

    def download_file(self, file_key, base_path):
        url = f"http://{self.fms_url}/{file_key}"
        try:
            with requests.get(url, stream=True) as r:
                file_extention = r.headers['x-ext'].replace('.','')
                file_location = os.path.join(base_path,f"{file_key}.{file_extention}")
                total_length = int(r.headers.get("Content-Length"))
                with tqdm.wrapattr(r.raw, "read", total=total_length, desc="")as raw:
                    with open(file_location, 'wb')as output:
                        shutil.copyfileobj(raw, output)
            return 'File Downloaded Successfully', file_key, r.headers, True
        except Exception as err:
            return self.get_response(url)

    def get_response(self, url):
        try:
            response = b''
            for response_bytes in requests.get(url).iter_lines():
                        response += response_bytes
            response = json.loads(response.decode('utf8').replace("'", '"'))
            response = response["message"]
            return response, 'Error', 'Error', False
        except:
            return "Error While Downloading File", 'Error', 'Error', False

    def upload_file(self, file_key, file_name, file_extention, base_path, group = None, created_by = None):
        try:
            url = f"http://{self.fms_url}/{file_key}"
            file_location = os.path.join(base_path,f"{file_name}.{file_extention}")
            headers = {'x-ext': file_extention, 'x-group': group, 'x-createdby': created_by}
            file_size = os.path.getsize(file_location)
            with open(file_location, 'rb') as file:
                with requests.post(url, headers=headers, data=file, stream=True) as req:
                    for chunk in tqdm(req.iter_content(chunk_size=4096),total=file_size,unit='B', unit_scale=True, unit_divisor=1024):
                        pass
            return "File Uploaded Successfully", True
        except Exception as err:
            return err, False

    def delete_file(self, file_key, ext, base_path): 
        os.remove(os.path.join(base_path,f"{file_key}.{ext}"))
        return f"File Deleted Successfully {file_key}.{ext}"


 