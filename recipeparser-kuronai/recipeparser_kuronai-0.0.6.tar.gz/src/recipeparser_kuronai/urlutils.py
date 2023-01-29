import urllib.request
import bs4 as bs
import json


def convert_to_dom(input_url):
    print(f'Parsing {input_url} to HTML...')
    request = prepare_request(input_url)
    html = urllib.request.urlopen(request).read()
    print('Finished parsing recipe!')
    dom = bs.BeautifulSoup(html, 'lxml')
    return dom


def prepare_request(input_url):
    header = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                            'AppleWebKit/537.11 (KHTML, like Gecko) '
                            'Chrome/23.0.1271.64 Safari/537.11',
              'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
              'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
              'Accept-Encoding': 'none',
              'Accept-Language': 'en-US,en;q=0.8',
              'Connection': 'keep-alive'}
    request = urllib.request.Request(input_url, headers=header)
    return request


def verify_url(input_url):
    print("Checking if recipe URL is supported...")
    try:
        dom = convert_to_dom(input_url)
    except:
        return False

    jsonified = get_json_metadata(dom)

    if not (jsonified["@type"] is None):
        types = jsonified["@type"]
        if types.index("Recipe") is not None:
            return True

    return False


def get_json_metadata(dom):
    script_jsld = dom.find("script", type='application/ld+json').text
    jsonified = json.loads(script_jsld)
    if type(jsonified) is list:
        jsonified = jsonified[0]

    return jsonified
