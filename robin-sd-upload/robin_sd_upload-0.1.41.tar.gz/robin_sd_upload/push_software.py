import os
import requests
import yaml
import json
from .get_bearer_token import get_bearer_token

def push_software(config, fpath, radarType, version_name):

    print('Getting the bearer token...')
    # check config file type
    if type(config) is not dict:
        return "Config file is not a dictionary"
    else:
        print('config type: ', type(config))
    # check config file
    print('config api_url: ', config['api_url'])

    request_url = config['api_url']

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
        print("ZIP not exist: " + fpath)
        return "ZIP not exist: " + fpath
        
    files = {
        'file': (fpath, open(fpath, 'rb'))
    }

    values = {
        'destination': json.dumps(radarType),
        'versionName': json.dumps(version_name)
    }
    
    print('Uploading software...')

    response = requests.post(request_url + '/api/softwares/softwarefiles', headers=headers, data=values, files=files)
    return response.json()