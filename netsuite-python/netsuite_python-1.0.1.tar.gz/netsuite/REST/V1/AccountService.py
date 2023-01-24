from netsuite_python.netsuite.REST.V1.mixins import RetrieveMixin, UpdateMixin


class AccountService(RetrieveMixin, UpdateMixin):
    api_url = "account/profile"

    def __init__(self, netsuite):
        super().__init__(netsuite)
