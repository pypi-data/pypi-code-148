from netsuite_python.netsuite.REST.V1.mixins import (CreateMixin, CreateCustomFieldMixin, ListMixin, ModelMixin, ReplaceMixin,
                                                     RetrieveMixin, UpdateMixin)


class OpportunityService(CreateMixin, CreateCustomFieldMixin, ListMixin, ModelMixin, ReplaceMixin, RetrieveMixin,
                         UpdateMixin):
    api_url = "opportunities"

    def __init__(self, netsuite):
        super().__init__(netsuite)
