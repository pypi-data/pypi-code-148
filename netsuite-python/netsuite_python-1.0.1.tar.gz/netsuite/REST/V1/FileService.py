from netsuite_python.netsuite.REST.V1.mixins import CreateMixin, DeleteMixin, ListMixin, RetrieveMixin, UpdateMixin


class FileService(CreateMixin, DeleteMixin, ListMixin, RetrieveMixin, UpdateMixin):
    api_url = "appointments"

    def __init__(self, netsuite):
        super().__init__(netsuite)
