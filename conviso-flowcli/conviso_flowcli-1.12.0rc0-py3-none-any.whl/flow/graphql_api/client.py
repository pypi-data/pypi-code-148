from urllib.parse import urlparse

import requests

from convisoappsec.version import __version__

from .error_handlers import GraphQlErrorHandler, RequestErrorHandler


class ConvisoGraphQLClient:
    DEFAULT_AUTHORIZATION_HEADER_NAME = 'x-api-key'
    DEFAULT_HEADERS = {}
    DEFAULT_API_PATH = '/graphql'

    def __init__(self, base_url, apikey=''):
        self.url = self.__mount_url(base_url)
        self.apikey = apikey
        self.DEFAULT_HEADERS.update(
            {
                self.DEFAULT_AUTHORIZATION_HEADER_NAME: apikey
            }
        )

        self.__low_client = GraphQLClient(self.url, self.DEFAULT_HEADERS)

    def query(self, query, variables={}):
        return self.__low_client.execute(query, variables)

    def __mount_url(self, base_url):
        parsed_url = urlparse(base_url)
        parsed_url = parsed_url._replace(path=self.DEFAULT_API_PATH)
        return parsed_url.geturl()


class GraphQLClient:
    DEFAULT_HEADERS = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }

    def __init__(self, url, headers={}):
        self.url = url
        self.__session = requests.Session()
        self.__session.headers.update(
            **self.DEFAULT_HEADERS,
            **headers
        )

    def execute(self, query, variables={}):
        try:
            payload = self._build_graphql_payload(query, variables)

            response = self.__session.post(
                url=self.url,
                json=payload,
            )

            response.raise_for_status()

        except Exception as e:
            handler = RequestErrorHandler(e)
            handler.handle_request_error()

        json_response = response.json()
        graphql_handler = GraphQlErrorHandler(json_response)
        graphql_handler.raise_on_graphql_error()
        graphql_handler.raise_on_graphql_body_error()

        return json_response['data']

    @staticmethod
    def _build_graphql_payload(query, variables):
        data = {
            'query': query,
            'variables': variables
        }

        return data
