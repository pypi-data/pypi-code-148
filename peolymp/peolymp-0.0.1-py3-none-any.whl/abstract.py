from peolymp.client import HTTPClient


class AbstractAPI:
    def __init__(self, username, password, space_id):
        self.space_id = space_id
        self.http_client = HTTPClient(username, password, space_id)

    def get_url(self):
        return "https://api.eolymp.com/spaces/" + self.space_id
