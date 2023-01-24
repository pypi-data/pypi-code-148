import requests
import json
from io import BytesIO
import pandas as pd
#from pyspark.sql.types import *
import os
#from pyspark.sql import DataFrame
#mport mestandardstz.util.global_variables as global_val




class Odk: #Odl_central_api/lib
    def __init__(self, odk_central_url: str):
        self.url = odk_central_url

    def get_access_token(self, email:str, password:str) -> str:
        credentials = json.dumps({"email": email, "password": password})
        login_url = self.url + "sessions"
        header = {'Content-Type': 'application/json'}
        login = requests.post(login_url, data=credentials, headers= header).json()
        if 'token' not in login:
            raise ConnectionRefusedError('Could not login and connect to odk server')
        access_token = login['token']
        return access_token
    
    
    def get_form_submission_dataframe(self, form_url:str, access_token:str) -> pd.DataFrame:
        data_url = self.url + form_url
        headers_ = {"Content-Type": "application/json", "Authorization": "Bearer " + access_token}
        submissions = requests.get(data_url, headers=headers_)
        csv_content_bytes = submissions.content
        csv_data = BytesIO(csv_content_bytes)
        data = pd.read_csv(csv_data)
        return data