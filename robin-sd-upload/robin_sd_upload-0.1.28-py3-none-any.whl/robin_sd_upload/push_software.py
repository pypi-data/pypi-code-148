import os
import requests
import json
from .get_bearer_token import get_bearer_token

def push_software(config, fpath, radarType, version_name):
    print('Getting the bearer token...')
    api_url = config['api_url']
    bearer_token = get_bearer_token(config)
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