import typing
from dataclasses import dataclass
import datetime

from sortme.group import Group

PREFIX = "/users"


@dataclass
class User:
    id: int
    handle: str
    name: str
    avatar: str
    bio: str
    registered_at: datetime.datetime

    @dataclass
    class Regal:
        @dataclass
        class RankRecord:
            rank: int
            updated: datetime.datetime

        @dataclass
        class Statistics:
            difficulties: tuple[int, int, int, int, int]
            total: int
            last_accepted: datetime.datetime

        @dataclass
        class Award:
            title: str
            type: int
            date: datetime.datetime

        rank_record: RankRecord
        statistics: Statistics
        awards: list[Award]

    regal: typing.Optional[Regal]

    rated: bool
    elite: bool
    cheater: bool


class Users(Group):
    def __init__(self, token, lang):
        super().__init__(token, lang)

    def get_by_handle(self, handle: typing.Union[str, int] = None) -> User:
        """
        Return general info about user by ID.

        :param handle: ID of user. If not provided, get info about current logged-in user.
        """

        if handle is None:
            handle = 0

        return self._make_request("GET", f"{PREFIX}/getByHandle", {"handle": handle}, data_class=User)
