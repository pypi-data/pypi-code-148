
from netsuite.swagger_client.configuration import Configuration
from netsuite import swagger_client
from netsuite.swagger_client.api import contact_api, customer_api


class RestClient:
    def __init__(self, netsuite):
        self.netsuite = netsuite
        self.configuration = Configuration()
        self.configuration.app_name = netsuite.netsuite_app_name
        self.configuration.access_token = netsuite.storage.get_access_token(netsuite.app_name)
        self.contact_api = contact_api.ContactApi(swagger_client.ApiClient(self.configuration))
        self.customer_api = customer_api.CustomerApi(swagger_client.ApiClient(self.configuration))
