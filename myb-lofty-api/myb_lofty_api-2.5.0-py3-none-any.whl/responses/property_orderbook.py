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


class OrderBook:
    def __init__(self, order_book_data: dict):
        self.buy_orders: list[BuyOrders] = [BuyOrders(item) for item in order_book_data.get('buyOrders')]
        self.sell_orders: list[SellOrders] = [SellOrders(item) for item in order_book_data.get('sellOrders')]


class Buy:
    def __init__(self, buy_data: dict):
        min: float = buy_data.get('min')
        self.min: Optional[Decimal] = Decimal(str(min)) if min is not None else None
        max: float = buy_data.get('max')
        self.max: Optional[Decimal] = Decimal(str(max)) if max is not None else None


class Sell:
    def __init__(self, sell_data: dict):
        min: float = sell_data.get('min')
        self.min: Optional[Decimal] = Decimal(str(min)) if min is not None else None
        max: float = sell_data.get('max')
        self.max: Optional[Decimal] = Decimal(str(max)) if max is not None else None


class Ranges:
    def __init__(self, ranges_data: dict):
        buy_data: dict = ranges_data.get('buy')
        self.buy: Buy = Buy(buy_data) if buy_data is not None else None
        sell_data: dict = ranges_data.get('sell')
        self.sell: Sell = Sell(sell_data) if sell_data is not None else None


class PropertyOrderbook:
    def __init__(self, property_orderbook_data: dict):
        self.property_id: str = property_orderbook_data.get('propertyId')
        order_book_data: dict = property_orderbook_data.get('orderBook')
        self.order_book: OrderBook = OrderBook(order_book_data) if order_book_data is not None else None
        ranges_data: dict = property_orderbook_data.get('ranges')
        self.ranges: Ranges = Ranges(ranges_data) if ranges_data is not None else None
