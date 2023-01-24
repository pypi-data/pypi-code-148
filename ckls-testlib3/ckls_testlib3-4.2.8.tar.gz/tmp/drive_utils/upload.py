from __future__ import print_function
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/media/ckl/dump/Documents/freelance/MOST_RECENT/jsl/jsl_internal_latest69696/python/tmp/secret.json"


import json

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from oauth2client import service_account

secret_path = '/media/ckl/dump/Documents/freelance/MOST_RECENT/jsl/jsl_internal_latest69696/python/tmp/secret.json'
token_path ='/media/ckl/dump/Documents/freelance/MOST_RECENT/jsl/jsl_internal_latest69696/python/tmp/token.json'


# gcp_json_credentials_dict = json.load(open(secret_path))#json.loads(secret_path)

# credentials = service_account.Credentials.from_service_account_info(gcp_json_credentials_dict)



def upload_basic():
    """Insert new file.
    Returns : Id's of the file uploaded

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    creds, _ = google.auth.default()

    try:
        # create drive api client
        service = build('drive', 'v3', credentials=creds)

        file_metadata = {'name': 'download.jpeg'}
        media = MediaFileUpload('download.jpeg',
                                mimetype='image/jpeg')
        # pylint: disable=maybe-no-member
        file = service.files().create(body=file_metadata, media_body=media,
                                      fields='id').execute()
        print(F'File ID: {file.get("id")}')

    except HttpError as error:
        print(F'An error occurred: {error}')
        file = None

    return file.get('id')


if __name__ == '__main__':
    upload_basic()