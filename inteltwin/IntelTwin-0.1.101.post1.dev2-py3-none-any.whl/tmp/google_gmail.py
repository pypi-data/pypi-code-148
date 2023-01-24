"""
Guides from Google
https://developers.google.com/gmail/api/guides
https://developers.google.com/workspace/guides/get-started

https://developers.google.com/gmail/api/quickstart/python

https://developers.google.com/gmail/api/guides/forwarding_settings

"""

from __future__ import print_function

import os.path
import logging
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://mail.google.com/',
          'https://www.googleapis.com/auth/gmail.addons.current.action.compose',
          'https://www.googleapis.com/auth/gmail.addons.current.message.action',
          'https://www.googleapis.com/auth/gmail.addons.current.message.metadata',
          'https://www.googleapis.com/auth/gmail.addons.current.message.readonly',
          'https://www.googleapis.com/auth/gmail.compose',
          'https://www.googleapis.com/auth/gmail.insert',
          'https://www.googleapis.com/auth/gmail.labels',
          'https://www.googleapis.com/auth/gmail.metadata',
          'https://www.googleapis.com/auth/gmail.modify',
          'https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.send',
          'https://www.googleapis.com/auth/gmail.settings.basic',
          'https://www.googleapis.com/auth/gmail.settings.sharing']


class GMailService:
    _file_google_api_creds: str = '/Users/vincent/.pythonbot/google_api_credentials.json'
    _file_access_token: str = '/Users/vincent/.pythonbot/google_token.json'
    _service_handle = None

    def __init__(self, google_api_creds: str = None, google_token: str = None):
        if google_api_creds is not None:
            self._file_google_api_creds = google_api_creds
        if google_token is not None:
            self._file_access_token = google_token

    def init_auth(self):
        _google_credentials: Credentials = None
        try:
            if os.path.exists(self._file_access_token):
                _google_credentials = Credentials.from_authorized_user_file(self._file_access_token, SCOPES)
            # If there are no (valid) credentials available, let the user log in.
            if not _google_credentials or not _google_credentials.valid:
                if _google_credentials and _google_credentials.expired \
                        and _google_credentials.refresh_token:
                    _google_credentials.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self._file_google_api_creds, SCOPES)
                    _google_credentials = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open(self._file_access_token, 'w') as file_token:
                    file_token.write(_google_credentials.to_json())
            self._service_handle = build('gmail', 'v1', credentials=_google_credentials)
            return self._service_handle
        except Exception as error:
            logging.error("Error Message:" + str(error), exc_info=True)
        return None

    def print_labels(self):
        labels = None
        try:
            if self._service_handle is not None:
                results = self._service_handle.users().labels().list(userId='me').execute()
                labels = results.get('labels', [])
            else:
                logging.warning("error : self._service_hande is None")

            if not labels:
                print('No labels found.')
                return
            print('Labels:')
            for label in labels:
                print(label)
                print(label['name'])

        except HttpError as error:
            # TODO(developer) - Handle errors from gmail API.
            logging.error("Error Message:" + error)

        return
