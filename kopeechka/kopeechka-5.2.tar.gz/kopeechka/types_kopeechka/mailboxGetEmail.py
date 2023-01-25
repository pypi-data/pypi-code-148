from kopeechka.errors import BAD_TOKEN, BAD_SITE, BAD_DOMAIN, BAD_BALANCE, SYSTEM_ERROR, OUT_OF_STOCK, TIME_LIMIT_EXCEED, UNKNOWN_ERROR

class MailboxGetEmail():
    def __init__(self, json: dict):
        self.data: dict = json
        self.status: str = self.data.get("status")
        self.id: str | None = self.data.get("id")
        self.mail: str | None = self.data.get("mail")
        self.value: str | None = self.data.get("value")
        if self.status == "ERROR":
            if self.value == "BAD_TOKEN":
                raise BAD_TOKEN(data=self.data)
            elif self.value == "BAD_SITE":
                raise BAD_SITE(data=self.data)
            elif self.value == "BAD_DOMAIN":
                raise BAD_DOMAIN(data=self.data)
            elif self.value == "BAD_BALANCE":
                raise BAD_BALANCE(data=self.data)
            elif self.value == "OUT_OF_STOCK":
                raise OUT_OF_STOCK(data=self.data)
            elif self.value == "SYSTEM_ERROR":
                raise SYSTEM_ERROR(data=self.data)
            elif self.value == "TIME_LIMIT_EXCEED":
                raise TIME_LIMIT_EXCEED(data=self.data)
