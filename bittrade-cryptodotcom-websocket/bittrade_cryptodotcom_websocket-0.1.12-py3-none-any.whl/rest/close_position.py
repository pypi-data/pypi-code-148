from typing import Any, Callable, Literal, Optional
from ..connection import wait_for_response
from ..models import (
    CryptodotcomResponseMessage,
    EnhancedWebsocket,
    CryptodotcomRequestMessage,
    EnhancedWebsocketBehaviorSubject
)
from reactivex import Observable, operators, disposable
from ..events import MethodName
from ccxt import cryptocom
from reactivex.scheduler import NewThreadScheduler

from returns.curry import curry


def order_confirmation(
    messages: Observable[CryptodotcomResponseMessage],
    exchange: cryptocom,
    order_id: str,
):
    def is_match(message: CryptodotcomResponseMessage) -> bool:
        try:
            return message.result["data"][0]["order_id"] == order_id
        except:
            return False

    return messages.pipe(
        operators.filter(is_match),
        operators.map(lambda x: (
            exchange.parse_order(x.result["data"][0])
        )),
    )


def close_position_factory(
    messages: Observable[CryptodotcomResponseMessage], exchange: cryptocom, socket: EnhancedWebsocketBehaviorSubject
) -> Callable[
    [str, Literal['market', 'limit'], Optional[str]], Observable
]:
    def close_position(
        symbol: str,
        type: Literal['market', 'limit'],
        price: Optional[str] = ''
    ):
        uppercase_type = type.upper()
        request = {
            "instrument_name": symbol,
            "type": uppercase_type
        }
        if (uppercase_type == "LIMIT") or (uppercase_type == "STOP_LIMIT"):
            request["price"] = exchange.price_to_precision(symbol, price)
        
        def subscribe(observer, scheduler=None):
            return messages.pipe(
                wait_for_response(
                    socket.value.send_message(
                        CryptodotcomRequestMessage(
                            MethodName.CLOSE_POSITION, params=request
                        )
                    ),
                    2.0,
                )
            ).subscribe(observer, scheduler=scheduler)
        return Observable(subscribe)
    return close_position
