from .group import Group
from .errors import *

from .groups import Users, Problems

HOSTNAME = "https://api.sort-me.org"


class API(Group):
    def __init__(self, token: str = None, lang: str = "ru"):
        super().__init__(token, lang)

        if token is not None:
            valid = self._make_request("GET", "/me", {})["valid"]
            if not valid:
                raise APIError("Wrong answe... token")

        self.users = Users(token, lang)
        self.problems = Problems(token, lang)
