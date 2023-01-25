from kopeechka.errors import BAD_TOKEN, NO_ACTIVATION, ACTIVATION_CANCELED, UNKNOWN_ERROR

class MailboxCancel():
    def __init__(self, json: dict):
        self.data: dict = json
        self.status: str = self.data.get("status")
        self.value: str | None = self.data.get("value")
        if self.status == "ERROR":
            if self.value == "BAD_TOKEN":
                raise BAD_TOKEN(data=self.data)
            elif self.value == "NO_ACTIVATION":
                raise NO_ACTIVATION(data=self.data)
            elif self.value == "ACTIVATION_CANCELED":
                raise ACTIVATION_CANCELED(data=self.data)
            else:
                raise UNKNOWN_ERROR(text=self.value, data=self.data)