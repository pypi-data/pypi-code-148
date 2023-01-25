"""
Module for various services via HTTP as a client
"""

import urllib
from urllib.request import urlopen
import urllib.request
import urllib.parse


class HTTPClientServices:
    """
    Class for various services via HTTP as a client
    Uses urllib module of the standard library of Python
    """
    def __init__(self, url):
        self.url = url

    def read_url(self, num_bytes):
        """
        reads the data from the url
        :param num_bytes: number of bytes that needs to be read
        """
        with urlopen(self.url) as webdata:
            print(webdata.read(num_bytes).decode('utf-8'))

    def get_request_to_url(self, data):
        """
        uses GET method to retrieve a URL
        :param data:  parameters of the URL - 'dict' type
        :raises HTTPError: when the specified URL is not found
        :raises TypeError: when the data passed is in wrong format
        """
        params = urllib.parse.urlencode(data)
        query_url = self.url + '?%s' % params
        with urlopen(query_url) as webdata:
            print(webdata.read().decode('utf-8'))

    def post_request_to_url(self, data):
        """
        uses POST method to retrieve a URL
        :param data:  parameters of the URL - 'dict' type
        :raises HTTPError: when the specified URL is not found
        :raises TypeError: when the data passed is in wrong format
        """
        data = urllib.parse.urlencode(data)
        data = data.encode('ascii')
        with urlopen(self.url, data) as webdata:
            print(webdata.read().decode('utf-8'))
