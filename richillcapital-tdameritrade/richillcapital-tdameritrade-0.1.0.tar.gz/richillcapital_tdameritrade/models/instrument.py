

class Instrument(object):
    """
    Represents instrument info from TD Ameritrade.
    """

    def __init__(self, symbol: str, description: str, exchange: str, asset_type: str, cusip: str) -> None:
        self.__symbol: str = symbol
        self.__description: str = description
        self.__exchange: str = exchange
        self.__asset_type: str = asset_type
        self.__cusip: str = cusip

    @property
    def symbol(self) -> str:
        return self.__symbol        

    @property
    def description(self) -> str:
        return self.__description