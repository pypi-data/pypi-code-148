import requests

def get_bearer_token(config_file):
    email_add = config_file['robin_email']
    password = config_file['robin_password']
    request_url = config_file['api_url']

    headers = {
        'Content-Type': 'application/json',
    }

    data = '{"email": "' + email_add + '", "password": "' + password + '"}'
    response = requests.post(request_url + '/api/auth/login', headers=headers, data=data)

    if response.status_code == 200:
        bearer_token = response.json()['token']
        print ("Bearer token: " + bearer_token)
        return bearer_token
    else:
        print("Error getting bearer token")
        return 1
