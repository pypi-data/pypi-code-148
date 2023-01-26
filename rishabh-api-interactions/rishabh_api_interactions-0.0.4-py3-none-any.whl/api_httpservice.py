# first api implementation

import urllib.request


class HttpService:
    def __init__(self):
        self._url = None
        self._file = None
        self._response = None

    def requesting_info(self, http_url, num_char=100):
        """ Method to fetch info from an url

        :param http_url: string obj containing the URL to be read
        :param num_char: int obj containing info of the number of characters to be read

        :return: string obj contains data to be returned
        """
        try:
            self._file = urllib.request.urlopen(http_url)
        except ValueError:
            return "URL NOT FOUND!!"

        self._response = self._file.read(num_char).decode('utf-8')
        return self._response


if __name__ == '__main__':
    url = "https://sixty-north.com/c/t.txt"
    print(HttpService().requesting_info(url))
