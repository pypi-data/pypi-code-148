from kopeechka.errors import BAD_TOKEN, NO_ACTIVATION, ACTIVATION_NOT_FOUND, BAD_EMAIL, SYSTEM_ERROR, UNKNOWN_ERROR

class MailboxReorder():
    def __init__(self, json: dict):
        self.data: dict = json
        self.status: str = self.data.get("status")
        self.id: str | None = self.data.get("id")
        self.mail: str | None = self.data.get("mail")
        self.value: str | None = self.data.get("value")
        if self.status == "ERROR":
            if self.value == "BAD_TOKEN":
                raise BAD_TOKEN(data=self.data)
            elif self.value == "NO_ACTIVATION":
                raise NO_ACTIVATION(data=self.data)
            elif self.value == "ACTIVATION_NOT_FOUND":
                raise ACTIVATION_NOT_FOUND(data=self.data)
            elif self.value == "BAD_EMAIL":
                raise BAD_EMAIL(data=self.data)
            elif self.value == "SYSTEM_ERROR":
                raise SYSTEM_ERROR(data=self.data)
