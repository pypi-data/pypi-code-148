import requests
import os
import yaml

bearer_token = ''
home_dir = os.path.expanduser("~")
config_file = home_dir + "/.config/robin/config.yaml"

with open("config.yml", "r") as file:
    config_file = yaml.safe_load(file)

#********** Credentials to login **********
robin_email = config_file['robin_email']
robin_password = config_file['robin_password']

# ********** API URL **********
api_url = config_file['api_url']

def get_bearer_token():
    headers = {
        'Content-Type': 'application/json',
    }

    data = '{"email": "' + robin_email + '", "password": "' + robin_password + '"}'
    response = requests.post(api_url + '/api/auth/login', headers=headers, data=data)

    bearer_token = response.json()['token']
    return bearer_token