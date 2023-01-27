import http.client
import json

class BaseWrapper:
    error = None

    def __init__(self, akamai=None):
        self.establish_connection()
        self.generate_headers(akamai)

    def establish_connection(self):
        self.connection = http.client.HTTPSConnection('www.tokopedia.com')

        return self.connection

    def generate_headers(self, akamai=None):
        self.headers = {
            'Content-Type': 'application/json'
        }

        if akamai:
            self.headers['X-TKPD-AKAMAI'] = akamai
        
        return self.headers

    @staticmethod
    def to_json(response):
        data = response.read()

        return json.loads(data.decode('utf-8'))

    def serialize(self):
        raise NotImplementedError