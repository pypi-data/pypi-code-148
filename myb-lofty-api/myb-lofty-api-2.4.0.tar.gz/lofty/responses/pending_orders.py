from decimal import Decimal
from typing import Optional


class BuyOrders:
    def __init__(self, buy_orders_data: dict):
        self.quantity: int = buy_orders_data.get('quantity')
        price: float = buy_orders_data.get('price')
        self.price: Optional[Decimal] = Decimal(str(price)) if price is not None else None
        self.property_id: str = buy_orders_data.get('propertyId')
        self.id: str = buy_orders_data.get('id')
        self.expire_at: int = buy_orders_data.get('expireAt')
        self.created_at: int = buy_orders_data.get('createdAt')


class SellOrders:
    def __init__(self, sell_orders_data: dict):
        self.quantity: int = sell_orders_data.get('quantity')
        price: float = sell_orders_data.get('price')
        self.price: Optional[Decimal] = Decimal(str(price)) if price is not None else None
        self.property_id: str = sell_orders_data.get('propertyId')
        self.id: str = sell_orders_data.get('id')
        self.expire_at: int = sell_orders_data.get('expireAt')
        self.created_at: int = sell_orders_data.get('createdAt')


class Data:
    def __init__(self, data: dict):
        # TODO: These types are a guess based on the property orderbook
        # TODO: There were no items in the lists when this endpoint was tested
        self.buy_orders: list[BuyOrders] = [BuyOrders(item) for item in data.get('buyOrders')]
        self.sell_orders: list[SellOrders] = [SellOrders(item) for item in data.get('sellOrders')]


class PendingOrders:
    def __init__(self, pending_orders_data: dict):
        self.property_id: str = pending_orders_data.get('propertyId')
        data_data: dict = pending_orders_data.get('data')
        self.data: Data = Data(data_data) if data_data is not None else None
