from kopeechka.errors import BAD_TOKEN, NO_ACTIVATION, UNKNOWN_ERROR

class MailboxGetFreshId():
    def __init__(self, json: dict):
        self.data: dict = json
        self.status: str = self.data.get("status")
        self.id: str | None = self.data.get("id")
        self.value: str | None = self.data.get("value")
        if self.status == "ERROR":
            if self.value == "BAD_TOKEN":
                raise BAD_TOKEN(data=self.data)
            elif self.value == "NO_ACTIVATION":
                raise NO_ACTIVATION(data=self.data)