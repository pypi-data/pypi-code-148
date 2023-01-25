class Zone():
    def __init__(self, json: dict):
        self.data: dict = json
        self.name: str = self.data.get("name")
        self.cost: int = self.data.get("cost")