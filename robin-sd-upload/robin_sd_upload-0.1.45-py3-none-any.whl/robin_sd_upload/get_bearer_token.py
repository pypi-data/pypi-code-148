import requests
import logging

def get_bearer_token(config):
    email_add = config['robin_email']
    password = config['robin_password']
    request_url = config['api_url']

    headers = {
        'Content-Type': 'application/json',
    }

    data = '{"email": "' + email_add + '", "password": "' + password + '"}'
    response = requests.post(request_url + '/api/auth/login', headers=headers, data=data)

    if response.status_code == 200:
        bearer_token = response.json()['token']
        logging.info("Bearer token: " + bearer_token)
        return bearer_token
    else:
        logging.error("Error getting bearer token")
        return 1
