from .email import Email
from kopeechka.errors import BAD_TOKEN, UNKNOWN_ERROR

class MailboxGetBulk():
    def __init__(self, json: dict):
        self.data: dict = json
        self.status: str = self.data.get("status")
        self.count: int | None = self.data.get("count")
        self.items: list | None = self.data.get("items")
        self.value: str | None = self.data.get("value")
        if self.status == "ERROR":
            if self.value == "BAD_TOKEN":
                raise BAD_TOKEN(data=self.data)
            else:
                raise UNKNOWN_ERROR(text=self.value, data=self.data)
        if self.items:
            self.items = [Email(data) for data in self.items]
        else:
            self.items = []