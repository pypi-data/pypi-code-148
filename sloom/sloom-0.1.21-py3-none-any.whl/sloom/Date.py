class Date:
    def __init__(self, dateString, origin) -> None:
        self._dateString = dateString
        self._origin = origin
        self.date = None
    
    def __str__(self) -> str:
        return self.date