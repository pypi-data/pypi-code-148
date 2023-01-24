from netsuite.REST.V1.mixins import (CreateMixin, ListMixin, ModelMixin, ReplaceMixin, RetrieveMixin)


class CompanyService(CreateMixin, ListMixin, ModelMixin, ReplaceMixin, RetrieveMixin):
    api_url = "companies"

    def __init__(self, netsuite):
        super().__init__(netsuite)
