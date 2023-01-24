from netsuite_python.netsuite.REST.V1.mixins import CreateMixin, ListMixin


class UserService(CreateMixin, ListMixin):
    api_url = "users"

    def __init__(self, netsuite):
        super().__init__(netsuite)

    def get_logged_in_user_info(self, **kwargs):
        return self._get(f"oauth/connect/userinfo", params=kwargs)

    def get_user_email_signature(self, user_id: int):
        return self._get(f"{self.api_url}/{user_id}/signature")
