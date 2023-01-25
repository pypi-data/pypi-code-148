class Email():
    def __init__(self, json: dict):
        self.data: dict = json
        self.id: int = self.data.get("id")
        self.service: str = self.data.get("service")
        self.email: str = self.data.get("email")
        self.date: int = self.data.get("date")
        self.status: str = self.data.get("status")
        self.value: str = self.data.get("value")
        self.comment: str = self.data.get("comment")
