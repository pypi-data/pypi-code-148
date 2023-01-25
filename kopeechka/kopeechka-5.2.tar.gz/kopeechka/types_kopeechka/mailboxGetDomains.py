from kopeechka.errors import BAD_TOKEN, UNKNOWN_ERROR

class MailboxGetDomains():
    def __init__(self, json: dict):
        self.data: dict = json
        self.status: str = self.data.get("status")
        self.count: int | None = self.data.get("count")
        self.domains: list | None = self.data.get("domains")
        self.value: str | None = self.data.get("value")
        if self.status == "ERROR":
            if self.value == "BAD_TOKEN":
                raise BAD_TOKEN(data=self.data)
            else:
                raise UNKNOWN_ERROR(text=self.value, data=self.data)