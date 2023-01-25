from typing import cast
from reactivex import Observable, operators
from ccxt import cryptocom

from ..connection import wait_for_response
from ..events import MethodName
from ..models import (
    CryptodotcomRequestMessage,
    CryptodotcomResponseMessage,
    EnhancedWebsocketBehaviorSubject,
)


def to_open_orders_entries(exchange: cryptocom):
    def to_open_orders_entries_(message: CryptodotcomResponseMessage):
        return cast(list[dict], exchange.parse_orders(message.result["data"]))
    return to_open_orders_entries_


def get_user_open_orders_factory(messages: Observable[CryptodotcomResponseMessage], socket: EnhancedWebsocketBehaviorSubject, exchange: cryptocom):
    def get_user_open_orders(instrument: str = "") -> Observable[list[dict]]:
        params = {"instrument_name": instrument} if instrument else {}
        return messages.pipe(
            wait_for_response(
                socket.value.send_message(
                    CryptodotcomRequestMessage(MethodName.GET_OPEN_ORDERS, params=params)
                )
            ),
            operators.map(to_open_orders_entries(exchange)),
        )
    return get_user_open_orders
