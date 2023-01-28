from eolymp.universe import universe_pb2, permission_pb2
from eolymp.universe.universe_http import UniverseClient

from peolymp.abstract import AbstractAPI


class UniverseAPI(AbstractAPI):
    def __init__(self, **kwargs):
        super(UniverseAPI, self).__init__(**kwargs)
        self.client = UniverseClient(self.http_client)

    def add_custom_admin_access(self, user_id):
        return self.client.GrantPermission(
            universe_pb2.GrantPermissionInput(space_id=self.space_id, role=permission_pb2.Permission.CUSTOM,
                                              user_id=user_id))
