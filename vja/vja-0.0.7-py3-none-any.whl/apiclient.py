import os
import requests
import click
import json
from functools import wraps
from vja import VjaError, config
from types import SimpleNamespace
import logging

logger = logging.getLogger(__name__)

# Expose the ApiClient and error classes for importing
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
                kwargs['access_token'] = self._token['access']
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
                self.get_access_token()
                kwargs['access_token'] = self._token['access']
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
        self._token = dict()
        self._token['access'] = None
        # caches
        self._cache = dict()
        self._cache['lists'] = None
        self._cache['labels'] = None
        self._cache['namespaces'] = None
        self._cache['tasks'] = None

    def create_url(self, path):
        return self._config['application']['api_url'] + path

    ###
    # Authentication
    ###
    def authenticate(self):
        """Use credentials to get userid and access token."""
        self.get_access_token()

    def load_access_token(self):
        """Load the access token from the file."""
        token_path = os.path.join(config.get_dir(), ApiClient._TOKEN_FILE)
        try:
            with open(token_path) as token_file:
                data = json.load(token_file)
        except (IOError):
            return False
        self._token['access'] = data['token']
        if not self._token['access']:
            return False
        return True

    def store_access_token(self):
        """Store the access token to the file."""
        token_path = os.path.join(config.get_dir(), ApiClient._TOKEN_FILE)
        data = {'token': self._token['access']}
        with open(token_path, 'w') as token_file:
            json.dump(data, token_file)


    @handle_http_error
    def get_access_token(self):
        """Get access token as specified in the API v3 docs."""
        if self.load_access_token():
            return
        url = self.create_url("/login")
        username = click.prompt("username")
        password = click.prompt("password", hide_input=True)
        payload = {'username': username,
                   'password': password}
        response = requests.post(url, json=payload)
        response.raise_for_status()
        self._token['access'] = response.json()['token']
        self.store_access_token()

    @handle_http_error
    def getJson(self, url, params=None):
        logger.debug("getJson: %s" % url)
        headers = {'Authorization': "Bearer {}".format(self._token['access'])}
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json(object_hook=lambda d: SimpleNamespace(**d))

    @check_access_token
    def getTasks(self, exclude_completed=True, **kwargs):
        if self._cache['tasks']:
            return self._cache['tasks']
        else:
            url=self.create_url("/tasks/all")
            params={'filter_by': 'done', 'filter_value': 'false'} if exclude_completed else None
            self._cache['tasks'] = self.getJson(url, params)
            return self._cache['tasks']

    @check_access_token
    def getLists(self, **kwargs):
        if self._cache['lists']:
            return self._cache['lists']
        else:
            url=self.create_url("/lists")
            self._cache['lists'] = self.getJson(url)
            return self._cache['lists']

    @check_access_token
    def getLabels(self, **kwargs):
        if self._cache['labels']:
            return self._cache['labels']
        else:
            url=self.create_url("/labels")
            self._cache['labels'] = self.getJson(url)
            return self._cache['labels']
