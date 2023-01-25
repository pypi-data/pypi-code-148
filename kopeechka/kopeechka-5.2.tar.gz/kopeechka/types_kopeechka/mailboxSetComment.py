from kopeechka.errors import BAD_TOKEN, NO_ACTIVATION, BAD_COMMENT, UNKNOWN_ERROR

class MailboxSetComment():
    def __init__(self, json: dict):
        self.data: dict = json
        self.status: str = self.data.get("status")
        self.value: str | None = self.data.get("value")
        if self.status == "ERROR":
            if self.value == "BAD_TOKEN":
                raise BAD_TOKEN(data=self.data)
            elif self.value == "NO_ACTIVATION":
                raise NO_ACTIVATION(data=self.data)
            elif self.value == "BAD_COMMENT":
                raise BAD_COMMENT(data=self.data)