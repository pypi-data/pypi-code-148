from netsuite.REST.V1.mixins import (CreateMixin, CreateCustomFieldMixin, DeleteMixin, ListMixin, ModelMixin, ReplaceMixin,
                                 RetrieveMixin, SearchMixin, UpdateMixin)


class TaskService(CreateMixin, CreateCustomFieldMixin, DeleteMixin, ListMixin, ModelMixin, ReplaceMixin,
                  RetrieveMixin, SearchMixin, UpdateMixin):
    api_url = "tasks"

    def __init__(self, netsuite):
        super().__init__(netsuite)
