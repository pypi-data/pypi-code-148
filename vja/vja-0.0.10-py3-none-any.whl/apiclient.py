import json
import logging
import os
from functools import wraps
from types import SimpleNamespace

import click
import requests

from vja import VjaError, config

logger = logging.getLogger(__name__)

__all__ = ['ApiClient']


def check_access_token(func):
    """ A decorator that makes the decorated function check for access token."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Provide decorated function with `access_token` provided as a keword
        argument.
        """
        # check if `access_token` is set to a value in kwargs
        if 'access_token' in kwargs and kwargs['access_token'] is not None:
            return func(*args, **kwargs)
        else:
            # try to get the access token
            try:
                self = args[0]
                self.get_access_token()
                return func(*args, **kwargs)
            # no access_token in kwargs or in class; die
            except KeyError:
                raise VjaError('need access token to call function %s;'
                               ' call authenticate()' % func.__name__)

    return wrapper


def handle_http_error(func):
    """A decorator to handle some HTTP errors raised in decorated function f."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        """Handle the HTTPError exceptions raised in f."""
        try:
            return func(*args, **kwargs)
        except requests.HTTPError as error:
            if error.response.status_code == 401 or error.response.status_code == 429:
                logger.info("HTTP-Error %s, url=%s; trying to retrieve new access token..."
                            % (error.response.status_code, error.response.url))
                self = args[0]
                self.get_access_token(force=True)
                return func(*args, **kwargs)  # try again with new token. Re-raise if failed.
            else:
                body = error.response.text
                logger.warning("HTTP-Error %s, url=%s body=%s"
                               % (error.response.status_code, error.response.url, body))
                raise

    return wrapper


class ApiClient(object):
    """Vikunja API client."""
    _TOKEN_FILE = 'token.json'

    def __init__(self, api_url):
        """Initialize a new ApiClient w/o auth credentials."""
        # config
        self._config = dict()
        self._config['application'] = dict()
        self._config['application']['api_url'] = api_url
        # OAuth2 tokens and scope
        self._user = None
        self._token = dict()
        self._token['access'] = None
        # caches
        self._cache = dict()
        self._cache['lists'] = None
        self._cache['labels'] = None
        self._cache['namespaces'] = None
        self._cache['tasks'] = None

    @property
    def user(self):
        """Property for accessing the cached user."""
        if self._user is None:
            raise KeyError('user not set! call authenticate()')
        return self._user

    @property
    def access_token(self):
        """Property for accessing the cached access token."""
        if not self._token['access']:
            raise KeyError('access token not set! call authenticate()')
        return self._token['access']

    def create_url(self, path):
        return self._config['application']['api_url'] + path

    ###
    # Authentication
    ###
    def authenticate(self):
        """Use credentials to get userid and access token."""
        self.get_access_token()
        self._user = self._user if self._user else self.get_user()

    def load_access_token(self):
        """Load the access token from the file."""
        token_path = os.path.join(config.get_dir(), ApiClient._TOKEN_FILE)
        try:
            with open(token_path) as token_file:
                data = json.load(token_file)
        except IOError:
            return False
        self._token['access'] = data['token']
        if not self._token['access']:
            return False
        return True

    def store_access_token(self):
        """Store the access token to the file."""
        token_path = os.path.join(config.get_dir(), ApiClient._TOKEN_FILE)
        data = {'token': self.access_token}
        with open(token_path, 'w') as token_file:
            json.dump(data, token_file)

    @handle_http_error
    def get_access_token(self, force=False):
        stored_token = self.load_access_token()
        if stored_token and not force:
            return
        if not force:
            logger.info("token.json not found. Getting new token")
        username = click.prompt("username")
        password = click.prompt("password", hide_input=True)
        payload = {'username': username,
                   'password': password}
        response = requests.post(self.create_url("/login"), json=payload)
        response.raise_for_status()
        self._token['access'] = response.json()['token']
        self.store_access_token()
        logger.info("Login successful.")

    @handle_http_error
    def get_json(self, url, params=None):
        headers = {'Authorization': "Bearer {}".format(self.access_token)}
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json(object_hook=lambda d: SimpleNamespace(**d))

    @check_access_token
    def get_user(self):
        return self.get_json(self.create_url("/user"))

    @check_access_token
    def get_tasks(self, exclude_completed=True):
        if self._cache['tasks']:
            return self._cache['tasks']
        else:
            url = self.create_url("/tasks/all")
            params = {'filter_by': 'done', 'filter_value': 'false'} if exclude_completed else None
            self._cache['tasks'] = self.get_json(url, params)
            return self._cache['tasks']

    @check_access_token
    def get_namespaces(self):
        if self._cache['namespaces']:
            return self._cache['namespaces']
        else:
            self._cache['namespaces'] = self.get_json(self.create_url("/namespaces"))
            return self._cache['namespaces']

    @check_access_token
    def get_lists(self):
        if self._cache['lists']:
            return self._cache['lists']
        else:
            self._cache['lists'] = self.get_json(self.create_url("/lists"))
            return self._cache['lists']

    @check_access_token
    def get_labels(self):
        if self._cache['labels']:
            return self._cache['labels']
        else:
            self._cache['labels'] = self.get_json(self.create_url("/labels"))
            return self._cache['labels']
