from .zone import Zone
from .popular import Popular
from kopeechka.errors import UNKNOWN_ERROR

class MailboxZones():
    def __init__(self, json: dict):
        self.data: dict = json
        self.status: str = self.data.get("status")
        if self.status == "ERROR":
            self.value: str = self.data.get("value")
            raise UNKNOWN_ERROR(text=self.value, data=self.data)
        if self.data.get("zones"):
            self.zones = self.data.get("zones")
        else:
            self.zones = []
        self.zones: list[Zone] = [Zone(data) for data in self.zones]
        if self.data.get("popular"):
            self.popular = self.data.get("popular")
        else:
            self.popular = []
        self.popular: list[Popular] = [Popular(data) for data in self.popular]

