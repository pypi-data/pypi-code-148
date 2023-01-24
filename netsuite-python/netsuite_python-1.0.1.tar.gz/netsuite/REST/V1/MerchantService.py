from netsuite_python.netsuite.REST.V1.mixins import ListMixin


class MerchantService(ListMixin):
    api_url = "merchants"

    def __init__(self, netsuite):
        super().__init__(netsuite)
