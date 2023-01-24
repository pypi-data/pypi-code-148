from netsuite_python.netsuite.REST.V1.mixins import ListMixin, RetrieveMixin


class TransactionService(ListMixin, RetrieveMixin):
    api_url = "transactions"

    def __init__(self, netsuite):
        super().__init__(netsuite)
