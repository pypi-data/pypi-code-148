import json
import logging
import sys
import time
import typing
from collections import OrderedDict
from copy import copy
from pprint import pformat
from uuid import uuid4

import requests
from six import wraps
from six.moves.urllib.parse import urljoin
from six.moves.urllib.parse import urlparse

logger = logging.getLogger(__name__)
MAX_RETRIES = 5
DEFAULT_TIMEOUT = 180


class ProviderHTTPClientException(Exception):
    def __init__(self, *args, **kwargs):
        super(ProviderHTTPClientException, self).__init__(*args)
        self.response = kwargs.get('response')
        for key, value in kwargs.items():
            setattr(self, key, value)


class RetryableException(ProviderHTTPClientException):
    pass


class ProviderHTTPServiceException(ProviderHTTPClientException):
    pass


def flatten_nested_object(obj, parent_key=''):
    result = {}

    for key, value in obj.items():
        if parent_key:
            new_key = '.'.join([parent_key, key])
        else:
            new_key = key

        if isinstance(value, list):
            raise ValueError('Nesting list is not supported yet. Please change key %s' % new_key)
        if isinstance(value, dict):
            result.update(flatten_nested_object(value, new_key))
        else:
            result[new_key] = value
    return result


# noinspection PyMethodMayBeStatic
class ProviderRequestProxy(object):
    def __init__(self, *, url, headers, timeout, retries=MAX_RETRIES, host=None, retry_delay=5, **kwargs):
        self.url = url
        self.headers = headers
        self.timeout = timeout
        self.retries = retries
        self.host = host
        self.raw = kwargs.get('raw', False)
        self.is_json = kwargs.get('json', True)
        self.retry_delay = retry_delay
        self.force_dict_order = kwargs.get('force_dict_order', sys.version_info < (3, 6))

    def augment_request_arguments(self, **request_kwargs):
        self.headers.update(request_kwargs.get('headers', {}))
        url_override = request_kwargs.get('url', None)
        self.url = self.url.format(**request_kwargs)

        data = {
            'url': url_override if url_override else self.url,
            'headers': self.headers,
            'timeout': self.timeout,
        }
        if 'data' in request_kwargs:
            data['data'] = request_kwargs['data']
        if 'json' in request_kwargs:
            data['json'] = request_kwargs['json']
        if 'files' in request_kwargs:
            data['files'] = request_kwargs['files']
        if 'stream' in request_kwargs:
            data['stream'] = request_kwargs['stream']
        if 'params' in request_kwargs:
            data['params'] = request_kwargs['params']

        if 'json' in data and 'data' in data:
            raise ValueError('You need to use either `json` or `data` parameter, not both.')

        if ('json' in data or 'data' in data) and 'files' in data:
            # parse json or data to enable multipart
            data_payload = data.pop('json', data.pop('data', None))

            if isinstance(data_payload, str):
                data_payload = json.load(data_payload)

            if isinstance(data_payload, list):
                raise ValueError('List json is not supported with Multipart')

            data['data'] = flatten_nested_object(data_payload)

        return data

    def get(self, **request_arguments):
        return self.request_with_retry('get', **request_arguments)

    def head(self, **request_arguments):
        return self.request_with_retry('head', **request_arguments)

    def options(self, **request_arguments):
        return self.request_with_retry('options', **request_arguments)

    def post(self, **request_arguments):
        return self.request_with_retry('post', **request_arguments)

    def put(self, **request_arguments):
        return self.request_with_retry('put', **request_arguments)

    def patch(self, **request_arguments):
        return self.request_with_retry('patch', **request_arguments)

    def delete(self, **request_arguments):
        return self.request_with_retry('delete', **request_arguments)

    def format_return_data(self, response):
        # TODO: decouple it
        if response.status_code == 204 or self.raw:
            return response
        elif self.is_json:
            try:
                if self.force_dict_order:
                    return response.json(object_pairs_hook=OrderedDict)
                else:
                    return response.json()
            except ValueError as e:
                if 'JSON' not in getattr(e, 'message', ''):
                    raise
                logger.exception('Failed to decode json file with error message: %s', e)
                return {}
        else:
            return response.content

    def set_file_caret_to_start(self, **request_arguments):
        files_in_request = request_arguments.get('files')
        if files_in_request:
            try:
                for key in files_in_request.keys():
                    files_in_request[key].seek(0)
            except Exception as exc:
                logger.debug('Failed to put file pointer to the start of the file with exc: %s', exc, exc_info=exc)

    def raise_if_error_status_code(self, response: requests.Response):
        if 400 <= response.status_code < 500:
            http_error_msg = '%s Client Error: %s for url: %s %s' % \
                             (response.status_code,
                              response.reason,
                              response.url,
                              response.content)
            raise ProviderHTTPClientException(http_error_msg, response=response)
        elif response.status_code in [502, 503]:
            raise RetryableException(
                'Deployment might be in progress, or server is overloaded',
                response=response
            )
        elif 500 <= response.status_code < 600:
            raise ProviderHTTPClientException('%d Server error. %s ' % (
                response.status_code,
                response.reason
            ), response=response)

    def request_with_retry(self, method, **request_arguments):
        request_arguments = self.augment_request_arguments(**request_arguments)
        retries = 0
        retry_errors = []
        response = None

        # if we say, that there should be no retries, put retries=0
        while retries < self.retries + 1:
            try:
                self.set_file_caret_to_start(**request_arguments)
                response = getattr(requests, method)(**request_arguments)
                self.raise_if_error_status_code(response)

            except (requests.Timeout, RetryableException) as exc:
                logger.debug('Retry request %s %s', method, request_arguments['url'])
                retries += 1
                retry_errors.append(exc)
                time.sleep(self.retry_delay)
            except requests.ConnectionError as exc:
                retry_errors.append(exc)
                raise ProviderHTTPServiceException('Service is not working with error: %s' % exc,
                                                   response=response)
            else:
                break  # Exits while loop
        else:
            raise ProviderHTTPServiceException('Failed to do request after {} tries'.format(len(retry_errors)),
                                               retries=retry_errors,
                                               response=response)

        return self.format_return_data(response)


class UniqueRequestProxy(ProviderRequestProxy):
    ENABLED_METHODS = ('post', 'put')

    def __init__(self,
                 *,
                 request_uid_header_name: str,
                 request_uid_value: typing.Callable[..., str] = None,
                 **kwargs):
        """
        :param request_uid_header_name: HTTP header name that will contain the
        request UUID
        :param request_uid_value: callable that will receive the request context and
        must return the string with UUID value; if callable is not provided or
        returned None, UUID will be generated automatically for every request
        """
        super(UniqueRequestProxy, self).__init__(**kwargs)

        self.header_name = request_uid_header_name
        self.uid_value = request_uid_value

    def inject_unique_request_header(self, **request_arguments):
        uuid_value = None
        if callable(self.uid_value):
            uuid_value = self.uid_value(**request_arguments)
        if uuid_value is None:
            uuid_value = str(uuid4())

        self.headers[self.header_name] = uuid_value

    def request_with_retry(self, method, **request_arguments):
        if method in self.ENABLED_METHODS:
            self.inject_unique_request_header(**request_arguments)

        return super(UniqueRequestProxy, self).request_with_retry(
            method,
            **request_arguments
        )

    def raise_if_error_status_code(self, response: requests.Response):
        # Handle "Another request is already processing" error with retry
        if response.status_code == 424:
            try:
                json_resp = response.json()
                error_desc = json_resp['error']
            except (ValueError, TypeError, KeyError):
                error_desc = 'Another request is already processing'
            raise RetryableException(error_desc, response=response)

        return super(UniqueRequestProxy, self).raise_if_error_status_code(response)


def remote_service(path, headers=None, timeout=None, json=True, raw=False, **options):
    if headers is None:
        headers = {}
    assert isinstance(headers, dict), 'Headers should be a dict!'

    # safe_methods = ['get', 'head', 'options']
    # unsafe_methods = ['post', 'put', 'patch', 'delete']

    def wrapper(func):
        @wraps(func)
        def inner(self, *args, **kwargs):
            if not isinstance(self, ReboticsBaseProvider):
                raise TypeError('This decorator should be used only for subclasses Rebotics Base Providers')

            provider = copy(self)

            authentication_headers = provider.get_provider_headers()
            headers.update(authentication_headers)

            url = provider.build_url(path)
            raw_override = kwargs.get('raw')
            proxy_opts = copy(provider.proxy_config)
            proxy_opts.update(options)

            session = provider.proxy_class(
                url=url,
                headers=headers,
                timeout=timeout or provider.timeout,
                retries=provider.retries,
                json=json,
                raw=raw_override or raw,
                host=provider.host,
                force_dict_order=provider.force_dict_order,
                **proxy_opts
            )

            provider.session = session
            self.session = session

            setattr(func, 'provider', provider)
            setattr(func, 'url', url)

            return func(provider, *args, **kwargs)

        return inner

    return wrapper


# noinspection PyMethodMayBeStatic
class ReboticsBaseProvider(object):
    retries = MAX_RETRIES
    timeout = DEFAULT_TIMEOUT
    proxy_class = ProviderRequestProxy
    proxy_config = {}  # additional parameters that will be passed to proxy_cls' init

    def __init__(self, host, **kwargs):
        self.host = host
        self.domain = urlparse(self.host).netloc
        self.headers = kwargs.get('headers', {})
        self.data = kwargs.get('data', {})
        self.session = None
        self.requests = requests

        if 'retries' in kwargs:
            self.retries = kwargs['retries']

        if 'timeout' in kwargs:
            self.timeout = kwargs['timeout']

        if 'token' in kwargs:
            self.set_token(kwargs['token'])

        self.role = kwargs.get('role', '')
        self.force_dict_order = kwargs.get('force_dict_order', sys.version_info < (3, 6))

    def get_provider_headers(self):
        return self.headers if self.headers else {}

    def set_header(self, key, value):
        self.headers[key] = value

    def set_token(self, token):
        self.headers['Authorization'] = 'Token %s' % token

    def build_url(self, path):
        return urljoin(self.host, path)

    @remote_service('/ping/', json=False)
    def ping(self, **kwargs):
        return self.session.get()

    @remote_service('/notifications/setWebhook/')
    def set_webhook(self, url, token=None):
        """Set webhook used by rebotics_sdk.hooks and rebotics_sdk.notification apps"""
        data = {
            'url': url
        }
        if token is not None:
            data['auth_token'] = token
        return self.session.post(data=data)

    def __repr__(self):
        return '<{} {}>'.format(self.__class__.__name__, pformat({
            'host': self.host,
            'headers': self.headers,
            'role': self.role
        }))

    def set_retailer_identifier(self, retailer_codename, retailer_secret_key):
        self.headers['x-retailer-codename'] = retailer_codename
        self.headers['x-retailer-secret-key'] = retailer_secret_key

    def is_retailer_identifier_used(self):
        header_keys = self.headers.keys()
        return ('x-retailer-codename' in header_keys) and ('x-retailer-secret-key' in header_keys)


class PageResult(dict):
    def __init__(self, json_data):
        """
        Returns paged result from rest framework
        :param dict json_data:
        """
        self.json_data = json_data
        super(PageResult, self).__init__(json_data)

    def __len__(self):
        return self.json_data['count']

    def __iter__(self):
        for item in self.json_data['results']:
            yield item

    def __getitem__(self, item):
        return self.json_data['results'][item]

    def __repr__(self):
        return "PageResult of {}".format(len(self))

    @property
    def pdf_download_url(self):
        return self.json_data.get('pdf_url')

    @property
    def next_page(self):
        return self.json_data['next']


class APIPageIterator:
    """
    Basic usage:
        iterator = APIPageIterator(provider.get_products_list, 1)
        for data in iterator:
            # do whatever with the data
            pass
    """
    def __init__(self, method, initial_page=1, **filter_params):
        self.method = method
        self.filter_params = filter_params  # page size can be passed as an optional value
        self.page = initial_page

    def __iter__(self):
        while True:
            page_result = self.method(page=self.page, **self.filter_params)

            yield from page_result

            if not page_result.next_page:
                break

            self.page += 1


def required_model_params(params=None):
    if params is None:
        params = ['model_path', 'index_path', 'meta_path']

    def outer(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            model_params = {
                key: kwargs[key] for key in params
            }
            kwargs['model_params'] = {
                'model_path': model_params['model_path'],
                'model_index_path': model_params['index_path'],
                'model_meta_path': model_params['meta_path']
            }
            result = func(*args, **kwargs)
            return result

        return wrapper

    if callable(params):
        return outer(params)

    return outer
