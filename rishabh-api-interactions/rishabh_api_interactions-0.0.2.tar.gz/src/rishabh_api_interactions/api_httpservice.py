# first api implementation

import urllib.request


def requesting_info(url, num_char=100):
    """ Method to fetch info from an url

    :param url: string obj containing the URL to be read
    :param num_char: int obj containing info of the number of characters to be read
    :return: string obj contains data to be returned
    """
    try:
        file = urllib.request.urlopen(url)
    except ValueError:
        return "URL NOT FOUND!!"

    response = file.read(num_char).decode('utf-8')
    return response


if __name__ == '__main__':
    url = "https://sixty-north.com/c/t.txt"
    print(requesting_info(url))
