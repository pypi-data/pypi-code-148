"""Manage HTTP requests and responses."""

import os
from urllib.parse import urlparse
from extension import EXTENSION_MAPPER

DEFAULT_FILE_PATH = "/index.html"

class Request:
    """Handle incoming requests"""

    def __init__(self, request) -> None:
        """Initialise the Request class

        :param host: string - the server host
        :param host: string - the server port
        :return tuple socket connection and host + port
        """
        self.request = request
        self.headers = request.split('\n')
        self.type = self.headers[0].split()[0]
        self.path = self.headers[0].split()[1]
        self.extension = ""

        print(self.type + ": " + self.path)

        self.set_file_path()

    def is_allowed_type(self) -> list:
        """Check if request is of allowed type

        :return boolean whether request is allowed
        """
        return self.type == 'GET'

    def set_file_path(self):
        """Set request file path

        :return None
        """
        parsed = urlparse(self.path)
        self.path = DEFAULT_FILE_PATH if parsed.path == "/" else parsed.path
        self.set_file_ext()

    def set_file_ext(self):
        """Set request file extension

        :return None
        """
        self.extension = os.path.splitext(self.path)[1] or ".html"

        if os.path.splitext(self.path)[1] == "":
            self.path += self.extension


class Response:
    """Handle outgoing response"""

    def __init__(self) -> None:
        """Initialise the Response class

        :return None
        """
        self.protocol = "HTTP/1.0 ".encode()
        self.code = "".encode()
        self.content_type = "\n".encode()
        self.response = "".encode()

    def set_success(self) -> None:
        """Set response success code

        :return None
        """
        self.code = "200 OK \n".encode()

    def set_404(self):
        """Set response 404 error code

        :return None
        """
        self.code = "404 File Not Found\n".encode()

    def set_405(self):
        """Set response 405 error code

        :return None
        """
        self.code = "405 Method not supported\n".encode()

    def set_content_type(self, content_type) -> None:
        """Set response content type

        :return None
        """

        if content_type in EXTENSION_MAPPER:
            self.content_type = ("Content-Type: " +
                                 EXTENSION_MAPPER[content_type] + "\n\n").encode()

    def set_content(self, content) -> None:
        """Set response content

        :return None
        """
        self.response += (content + "\n\n".encode())

    def set_header(self, headers: list) -> None:
        """Set response header

        :return None"""
        for header in headers:
            self.response += (header + "\n\n").encode()

    def get_response(self) -> bytes:
        """Return response

        :return bytes - response
        """
        return self.protocol + self.code + self.content_type + self.response
