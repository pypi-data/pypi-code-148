from kopeechka.errors import BAD_TOKEN, WAIT_LINK, NO_ACTIVATION, ACTIVATION_CANCELED, UNKNOWN_ERROR

class MailboxGetMessage():
    def __init__(self, json: dict):
        self.data: dict = json
        self.status: str = self.data.get("status")
        self.value: str | None = self.data.get("value")
        self.fullmessage: str | None = self.data.get("fullmessage")
        if self.status == "ERROR":
            if self.value == "BAD_TOKEN":
                raise BAD_TOKEN(data=self.data)
            elif self.value == "WAIT_LINK":
                raise WAIT_LINK(data=self.data)
            elif self.value == "NO_ACTIVATION":
                raise NO_ACTIVATION(data=self.data)
            elif self.value == "ACTIVATION_CANCELED":
                raise ACTIVATION_CANCELED(data=self.data)
