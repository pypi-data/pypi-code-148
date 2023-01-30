import struct
from ctypes import Structure, c_int64, c_uint64, c_double, c_float, c_uint32

from .types import TickObject
from .types import register_type, register_object
from .varint import encode, decode_bytes

# TODO
class RawOrderBook(TickObject):
    def __init__(self):
        return


class RawOBDelta(Structure):
    _fields_ = [("part1", c_uint64), ("part2", c_uint64)]


# TODO
class RawTrade(TickObject):
    def __init__(self):
        return


class RawTradeDelta(Structure):
    _fields_ = [("part1", c_uint64), ("part2", c_uint64)]


class Int64(TickObject):
    def __init__(self, val=None):
        self.value = val

    def to_snapshot(self):
        return encode(self.value)

    def from_snapshot(self, snapshot):
        self.value = decode_bytes(snapshot)

    def deltas_to(self, tobject):
        # Need to return a pointer to slice ?
        # Need to return an array of structure
        return [c_int64(tobject.value)]

    def process_deltas(self, deltas):
        # deltas is an iterable of delta
        delta = deltas[len(deltas) - 1]

        # delta must be a c_int64
        self.value = delta.value

    def clone(self):
        return Int64(self.value)


class UInt64(TickObject):
    def __init__(self, val=None):
        self.value = val

    def to_snapshot(self):
        return encode(self.value)

    def from_snapshot(self, snapshot):
        self.value = decode_bytes(snapshot)

    def deltas_to(self, tobject):
        # Need to return a pointer to slice ?
        # Need to return an array of structure
        return [c_uint64(tobject.value)]

    def process_deltas(self, deltas):
        # deltas is an iterable of delta
        delta = deltas[len(deltas) - 1]

        # delta must be a c_uint64
        self.value = delta.value

    def clone(self):
        return UInt64(self.value)


class UInt64Sum(UInt64):
    pass


class Float64(TickObject):
    def __init__(self, val=None):
        self.value = val

    def to_snapshot(self):
        return struct.pack('d')

    def from_snapshot(self, snapshot):
        self.value = struct.unpack('d', snapshot)[0]

    def deltas_to(self, tobject):
        # Need to return a pointer to slice ?
        # Need to return an array of structure
        return [c_double(tobject.value)]

    def process_deltas(self, deltas):
        if len(deltas) == 0:
            return
        # deltas is an iterable of delta
        delta = deltas[len(deltas) - 1]

        # delta must be a c_int64
        self.value = delta.value

    def clone(self):
        return Float64(self.value)


class OBPrice(TickObject):
    def __init__(self, depth=None, price=None, weight=None):
        self.depth = depth
        self.price = price
        self.weight = weight

    def to_snapshot(self):
        return encode(self.price)

    def from_snapshot(self, snapshot):
        self.price = struct.unpack('d', snapshot[:8])[0]
        self.weight = struct.unpack('d', snapshot[8:])[0]

    def deltas_to(self, tobject):
        # Need to return a pointer to slice ?
        # Need to return an array of structure
        return [OBPriceDelta(price=tobject.price, weight=tobject.weight)]

    def process_deltas(self, deltas):
        # deltas is an iterable of delta
        if len(deltas) == 0:
            return
        delta = deltas[len(deltas) - 1]

        # delta must be a c_int64
        self.price = delta.price
        self.weight = delta.weight

    def clone(self):
        return OBPrice(depth=self.depth, price=self.price, weight=self.weight)


class OBPriceDelta(Structure):
    _fields_ = [("price", c_double), ("weight", c_double)]


class Trade(TickObject):
    def __init__(self, price=None, size=None):
        self._price = price
        self._size = size

    def from_snapshot(self, snapshot):
        self._price = struct.unpack('d', snapshot[:8])[0]
        self._size = struct.unpack('d', snapshot[8:])[0]

    def to_snapshot(self):
        # TODO
        return None

    def process_deltas(self, deltas):
        # deltas is an iterable of delta
        delta = deltas[len(deltas) - 1]

        # delta must be a c_int64
        self._price = delta.price
        self._size = delta.size

    def deltas_to(self, tobject):
        # Need to return a pointer to slice ?
        # Need to return an array of structure
        return [TradeDelta(price=tobject._price, size=tobject._size)]

    def clone(self):
        return Trade(price=self._price, size=self._size)

    def price(self):
        return self._price

    def size(self):
        return self._size


class TradeDelta(Structure):
    _fields_ = [("price", c_double), ("size", c_double)]


class OBOrder(TickObject):
    def __init__(self, price=None, size=None, queue=None):
        self.price = price
        self.size = size
        self.queue = queue

    def from_snapshot(self, snapshot):
        self.price = struct.unpack('d', snapshot[:8])[0]
        self.size = struct.unpack('d', snapshot[8:16])[0]
        self.queue = struct.unpack('d', snapshot[16:])[0]

    def to_snapshot(self):
        # TODO
        return None

    def process_deltas(self, deltas):
        # deltas is an iterable of delta
        delta = deltas[len(deltas) - 1]

        # delta must be a c_int64
        self.price = delta.price
        self.size = delta.size
        self.queue = delta.queue

    def deltas_to(self, tobject):
        # Need to return a pointer to slice ?
        # Need to return an array of structure
        return [OBOrderDelta(price=tobject.price, size=tobject.size, queue=tobject.queue)]

    def clone(self):
        return OBOrder(price=self.price, size=self.size, queue=self.queue)


class OBOrderDelta(Structure):
    _fields_ = [("price", c_double), ("size", c_double), ("queue", c_double)]


class OHLCV(TickObject):
    def __init__(self, o=None, h=None, l=None, c=None, buy_count=None, sell_count=None, buy_vol=None, sell_vol=None,
                 price=None):
        self.o = o
        self.h = h
        self.l = l
        self.c = c
        self.buy_count = buy_count
        self.sell_count = sell_count
        self.buy_vol = buy_vol
        self.sell_vol = sell_vol
        self.price = price

    def from_snapshot(self, snapshot):
        self.o = struct.unpack('f', snapshot[:4])[0]
        self.h = struct.unpack('f', snapshot[4:8])[0]
        self.l = struct.unpack('f', snapshot[8:12])[0]
        self.c = struct.unpack('f', snapshot[12:16])[0]
        self.buy_count = struct.unpack('I', snapshot[16:20])[0]
        self.sell_count = struct.unpack('I', snapshot[20:24])[0]
        self.buy_vol = struct.unpack('f', snapshot[24:28])[0]
        self.sell_vol = struct.unpack('f', snapshot[28:32])[0]
        self.price = struct.unpack('f', snapshot[32:36])[0]

    def to_snapshot(self):
        # TODO
        return None

    def process_deltas(self, deltas):
        # deltas is an iterable of delta
        delta = deltas[len(deltas) - 1]

        # delta must be a c_int64
        self.o = delta.o
        self.h = delta.h
        self.l = delta.l
        self.c = delta.c
        self.buy_count = delta.buy_count
        self.sell_count = delta.sell_count
        self.buy_vol = delta.buy_vol
        self.sell_vol = delta.sell_vol
        self.price = delta.price

    def deltas_to(self, tobject):
        # Need to return a pointer to slice ?
        # Need to return an array of structure
        return []

    def clone(self):
        return OHLCV()


class OHLCVDelta(Structure):
    _fields_ = [
        ("o", c_float),
        ("h", c_float),
        ("l", c_float),
        ("c", c_float),
        ("buy_count", c_uint32),
        ("sell_count", c_uint32),
        ("buy_vol", c_float),
        ("sell_vol", c_float),
        ("price", c_float)
    ]


class NewLiquidation(TickObject):
    def __init__(self, price=None, quantity=None):
        self._price = price
        self._quantity = quantity

    def from_snapshot(self, snapshot):
        self._price = struct.unpack('d', snapshot[0:8])[0]
        self._quantity = struct.unpack('d', snapshot[8:16])[0]

    def to_snapshot(self):
        return None

    def process_deltas(self, deltas):
        delta = deltas[len(deltas) - 1]
        self._price = delta.Price
        self._quantity = delta.Quantity

    def deltas_to(self, tobject):
        return []

    def clone(self):
        return NewLiquidation(price=self._price, quantity=self._quantity)

    def price(self):
        return abs(self._price)

    def size(self):
        if self._price < 0:
            return self._quantity * -1
        else:
            return self._quantity


class NewLiquidationDelta(Structure):
    _fields_ = [('Price', c_double), ('Quantity', c_double)]


class AggLiquidity(TickObject):
    def __init__(self, map=None, ts=None):
        self.map = map
        self.ts = ts

    def __chunker(self, l, size):
        return (l[pos:pos + size] for pos in range(0, len(l), size))

    def from_snapshot(self, snapshot):
        self.ts = struct.unpack('d', snapshot[0:8])[0]
        self.map = {}
        for byte in self.__chunker(snapshot[16:], 16):
            value = struct.unpack('d', byte[0:8])[0]
            key = struct.unpack('q', byte[8:16])[0]
            self.map[key] = value

    def process_deltas(self, deltas):
        if len(deltas) == 0:
            return
        max_int = 9223372036854775807
        for d in deltas:
            if d.Key == max_int:
                self.ts = d.Quantity
                continue
            self.map[d.Key] = d.Quantity

    def deltas_to(self, tobject):
        return []

    def clone(self):
        return AggLiquidity(map=self.map, ts=self.ts)

    def to_snapshot(self):
        return None


class AggLiquidityDelta(Structure):
    _fields_ = [('Quantity', c_double), ('Key', c_int64)]


register_type("Int64", Int64, c_int64)
register_type("UInt64", UInt64, c_uint64)
register_type("Float64", Float64, c_double)
register_type("RawOrderBook", RawOrderBook, RawOBDelta)
register_type("RawTrade", RawTrade, RawTradeDelta)
register_type("OBPrice", OBPrice, OBPriceDelta)
register_type("Trade", Trade, TradeDelta)
register_type("BuyTrade", Trade, TradeDelta)
register_type("SellTrade", Trade, TradeDelta)
register_type("OBOrder", OBOrder, OBOrderDelta)
register_type("MidPrice", Float64, c_double)
register_type("Log", Float64, c_double)
register_type("TradeImbalance", Float64, c_double)
register_type("OBImbalance", Float64, c_double)
register_type("OHLCV", OHLCV, OHLCVDelta)
register_type("OBLiquidity", Float64, c_double)
register_type("NewLiquidation", NewLiquidation, NewLiquidationDelta)
register_type("AggLiquidity", AggLiquidity, AggLiquidityDelta)

register_object("UInt64Sum", "UInt64")
register_object("Float64", "Float64")
register_object("Float64Average", "Float64")
register_object("Float64Median", "Float64")
register_object("CombinedOBPrice", "Float64")
register_object("OBPrice", "OBPrice")
register_object("MidPrice", "MidPrice")
register_object("Trade", "Trade")
register_object("BuyTrade", "Trade")
register_object("SellTrade", "Trade")
register_object("BestBid", "OBPrice")
register_object("BestAsk", "OBPrice")
register_object("OHLCV", "OHLCV")
register_object("NewLiquidation", "NewLiquidation")
register_object("AggOHLCV", "OHLCV")
register_object("AggOBLiquidity", "AggLiquidity")
