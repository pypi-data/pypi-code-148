"""Module is used for making api requests and getting file
    info from url
"""

import json
from pprint import pprint
from urllib.request import urlopen
from urllib.error import HTTPError

# REST api interaction function
def http_request(url="", data=None, timeout=30):
    """Function returns result and status code for url request provided
        POST request will be made if data is not None otherwise a GET request
        will be made to the url

        ARGS:
            url: url for making api request
            data: data to be sent to url expected to be a dictionary
            timeout: stop listening for request after timeout seconds
    """
    if len(url) == 0:
        raise ValueError("url must not be empty")

    # Checking for correct data type
    if data is not None and not isinstance(data, dict):
        raise TypeError("data must be a dictionary")

    # Encoding data to utf-8 format to send over http
    if data is not None:
        data = json.dumps(data).encode('utf-8')

    try:
        response = urlopen(url=url, data=data, timeout=timeout)
    except HTTPError:
        return {
            "message": "Invalid request",
            "status": 405
        }

    if response.getcode() != 200:
        return {
            "message": "Error Occured",
            "status": response.getcode()
        }

    result = []

    decoded_data = json.loads(response.readline().decode('utf-8'))

    while True:
        result.append(decoded_data)
        try:
            decoded_data = json.loads(response.readline().decode('utf-8'))
        except json.decoder.JSONDecodeError:
            break

    return {
        "result": result,
        "status": 200
    }


def get_file_data(url="", timeout=30):
    """Function will get the data from the provided url, decode it and
        return each line as an element of a list

        ARGS:
            url: url to get the file data
            timeout: stop listening for request after timeout seconds
        """
    if len(url) == 0:
        raise ValueError("url must not be empty")

    result = []

    with urlopen(url=url, timeout=timeout) as file:
        for line in file.readlines():
            result.append(line.decode('utf-8'))

    return result

if __name__ == "__main__":
    res = http_request("https://api.coindesk.com/v1/bpi/currentprice.json")
    pprint(res)

    res = get_file_data(url="https://raw.githubusercontent.com/Vinesh0299/python-learning/main/ssh_day3.py")
    pprint(res)
