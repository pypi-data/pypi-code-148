import io
import zipfile

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry


class Client:
    """ Client class for performing HTTP requests.

    Attributes:
        session (requests.Session): session object used to make HTTP requests.
    """

    def __init__(self, max_retries=5, backoff_factor=1.0):
        """ Initializes object attributes.

        Args:
            max_retries: Maximum number of times to retry an http request on encountering specific errors.
            backoff_factor: Determines time between retries. The formula for the waiting time between two retries
                (except for the first one which is immediate) is: backoff_factor * 2 ** (retry_number).
        """
        self.session = requests.Session()
        self.session.mount('https://', self._retry_adapter(max_retries=max_retries, backoff_factor=backoff_factor))

    @staticmethod
    def _retry_adapter(max_retries=5, backoff_factor=1.0, status_forcelist=(429, 500, 501, 502, 503, 504)):
        """ Builds a HTTPAdapter that can be mounted on a session object to retry requests after specific errors.

        Args:
            max_retries: Maximum number of retries.
            backoff_factor: The formula for the waiting time between two retries (except for the first one which is
                immediate) is: backoff_factor * 2 ** (retry_number).

        Returns:
            An HTTPAdapter object.
        """
        retry = Retry(
            total=max_retries,
            read=max_retries,
            connect=max_retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist
        )
        return HTTPAdapter(max_retries=retry)

    def download_zip(self, url: str) -> zipfile.ZipFile:
        """ Downloads a zip file from a URL and returns a ZipFile object."""
        return zipfile.ZipFile(io.BytesIO(self.download_file(url=url)))

    def extract_zip_url(self, url: str, zip_extract_path: str):
        """ Downloads a zip file and extracts all its contents to the directory specified by <zip_extract_path>."""
        zip_file = self.download_zip(url)
        zip_file.extractall(zip_extract_path)

    def download_file(self, url: str, stream: bool = False) -> bytes:
        """ Downloads a file from a URL

        Args:
            url: The URL of the file.
            stream: A Boolean indication if the response should be immediately downloaded (False) or streamed (True).

        Returns:
            The file's content as a byte array.
        """
        return self._request(method='GET', url=url, stream=stream).content

    def _request(self, method: str, url: str, stream: bool = False) -> requests.Response:
        """ A wrapper around the requests.request() method.

        Args:
            method: The method to use for the request (i.e. POST or GET).
            url: The URL string for the request
            stream: A Boolean indication if the response should be immediately downloaded (False) or streamed (True).

        Returns:
            A requests.Response object.

        Raises:
            HTTPError in case the response does not result in HTTP status code 200.
        """
        response = requests.request(method=method, url=url, stream=stream)
        response.raise_for_status()
        return response
