import os
import requests
import json
import yaml
from .get_bearer_token import get_bearer_token

radarType = ''
# version_name = ''
# bearer_token = ''

home_dir = os.path.expanduser("~")
config_file = home_dir + "/.config/robin/config.yaml"


#********** Credentials to login from config.yml **********
with open("config.yml", "r") as file:
    config_file = yaml.safe_load(file)

robin_email = config_file['robin_email']
robin_password = config_file['robin_password']
api_url = config_file['api_url']

def push_software(fpath, radarType, version_name):
    print('Getting the bearer token...')
    # print('PS robin_email: ', robin_email)
    # print('PS robin_password: ', robin_password)
    # print('PS api_url: ', api_url)

    bearer_token = get_bearer_token()
    headers = {
        'Authorization': 'Bearer ' + bearer_token,
    }
    if not bearer_token:
        return "Bearer token is empty"
    else:
        print('bearer_token: ', bearer_token)

    # check if can open file path
    if os.path.isfile(fpath):
        print("ZIP file exists: " + fpath)
    else:
        return "ZIP not exist: " + fpath
        
    files = {
        'file': (fpath, open(fpath, 'rb'))
    }

    values = {
        'destination': json.dumps(radarType),
        'versionName': json.dumps(version_name)
    }
    
    print('Uploading software...')

    response = requests.post(api_url+'/api/softwares/softwarefiles', headers=headers, data=values, files=files)
    return response.json()