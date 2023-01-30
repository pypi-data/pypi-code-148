import requests
import filetype

from typing import Union


class Model:
    def __init__(self, api_key: str):
        self.model = None
        self.endpoint = None
        self.background_job = None
        self.beautify = False
        self.base_domain = "https://api.server.cameralyze.co"
        self.api_key = api_key
        
    def beautify_response(self):
        self.beautify = True
        
    def set_model(self, model: str):
        """
        Args:
            model (str): Model UUID or model alias name
        """
        self.model = model
        
    def set_endpoint(self, endpoint: str):
        """
        Args:
            endpoint (str): Endpoint UUID or endpoint alias name
        """
        self.endpoint = endpoint
        
    def set_background_job(self, background_job: str):
        """
        Args:
            background_job (str): Background job UUID or background job alias name
        """
        self.background_job = background_job
    
    def read_file(self, path: str) -> tuple:
        file_type = filetype.guess(path).mime
        response = requests.post(
            "https://platform.api.cameralyze.com/application/builder/file/create",
            json={"apiKey": self.api_key, "fileType": file_type}
        ).json()
        upload_url = response["url"]
        file_id = response["file_id"]

        with open(path, 'rb') as local_file:
            local_file_body = local_file.read()

        requests.put(
            upload_url, 
            data=local_file_body, 
            headers={'Content-Type': file_type, 'x-amz-acl': 'public-read'}
        )

        return file_id, file_type

    def __get_json(self, image: Union[str, tuple]) -> dict:
        json={"apiKey": self.api_key, "rawResponse": not self.beautify}

        if isinstance(image, tuple):
            json["fileId"] = image[0]
            json["fileType"] = image[1]
        elif image.startswith("http"):
            json["url"] = image
        else:
            json["image"] = image
            
        if self.endpoint:
            json["applicationUuid"] = self.endpoint
        
        if self.background_job:
            json["applicationUuid"] = self.background_job
        
        return json
    
    def __get_path(self) -> str:
        if self.endpoint:
            return "endpoint"
        
        if self.background_job:
            return "job"
        
        return "model"
    
    def __get_unique_id(self) -> str:
        if self.endpoint:
            return self.endpoint
        
        if self.background_job:
            return self.background_job
        
        return self.model

    def predict(self, image: Union[str, tuple]) -> dict:
        api_call = requests.post(
            "{base_domain}/{path}/{unique_id}".format(base_domain=self.base_domain, path=self.__get_path(), unique_id=self.__get_unique_id()),
            json=self.__get_json(image=image)
        )

        return api_call.json() 
