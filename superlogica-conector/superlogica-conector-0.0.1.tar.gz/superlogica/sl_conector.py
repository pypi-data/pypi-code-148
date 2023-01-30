import requests

class SLConector():

    def __init__(self) -> None:
        self.headers = None
        self.method= None,
        self.url= None,
        self.params= None

    def add_headers(self, api_key, token) -> None:
        self.headers = {
            'Content-Type': 'application/json',
            'app_token': api_key,
            'access_token': token
        }

    def add_params(self, method, url, **kwargs) -> None:
        self.method = method
        self.url = url
        self.params = kwargs

    def results(self, pages):
        page = 1

        while page <= pages:
            self.params['pagina'] = page
            page = page + 1
            try:
                response = requests.request(
                    method = 'GET',
                    url = self.url,
                    headers = self.headers,
                    params = self.params
                )
                results = response.json()

                if len(results) > 0:
                    yield results
                else:
                    yield []
            except Exception as error:
                raise Exception(f"Error found in request: {error}")

