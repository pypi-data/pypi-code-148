from netsuite_python.netsuite.REST.V1.mixins import CreateMixin, ListMixin, ModelMixin


class SubscriptionService(CreateMixin, ListMixin, ModelMixin):
    api_url = "subscriptions"

    def __init__(self, netsuite):
        super().__init__(netsuite)
