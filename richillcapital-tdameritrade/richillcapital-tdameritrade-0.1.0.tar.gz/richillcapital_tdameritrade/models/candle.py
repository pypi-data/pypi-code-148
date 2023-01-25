

class Candle(object):
    """
    Represents candle data from TD Ameritrade.
    """
    
    def __init__(self, symbol: str, timestamp: int, open: float, high: float, low: float, close: float, volume: int) -> None:
        self.__symbol: str = symbol
        self.__timestamp: int = timestamp
        self.__open: float = open
        self.__high: float = high
        self.__low: float = low
        self.__close: float = close
        self.__volume: int = volume

    @property
    def symbol(self) -> str:
        return self.__symbol

    @property
    def timestamp(self) -> int:
        return self.__timestamp

    @property
    def open(self) -> float:
        return self.__open

    @property
    def high(self) -> float:
        return self.__high

    @property
    def low(self) -> float:
        return self.__low
        
    @property
    def close(self) -> float:
        return self.__close

    @property
    def volume(self) -> int:
        return self.__volume    

    def __repr__(self) -> str:
        return f"Symbol: {self.symbol} Timestamp: {self.timestamp} Open: {self.open} High: {self.high} Low: {self.low} Close: {self.close}"
            