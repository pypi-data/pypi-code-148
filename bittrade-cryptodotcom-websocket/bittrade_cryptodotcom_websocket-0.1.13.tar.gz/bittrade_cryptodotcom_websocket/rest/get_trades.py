from logging import getLogger
from typing import Callable, Optional
from reactivex import Observable, defer, operators, just
from ccxt import cryptocom

from ..connection import wait_for_response
from elm_framework_helpers.output import info_operator
from ..events import MethodName
from ..models import (
    CryptodotcomRequestMessage,
    CryptodotcomResponseMessage,
    EnhancedWebsocketBehaviorSubject,
    Trade
)
logger = getLogger(__name__)


def get_trades_factory(response_messages: Observable[CryptodotcomResponseMessage], exchange: cryptocom, ws: EnhancedWebsocketBehaviorSubject):
    def get_trades(symbol: str, count: Optional[int] = 25):
        instrument_name = exchange.market(symbol)['id']
        def get_trades_(*_) -> Observable[list[Trade]]:
            if not ws.value:
                logger.error('No websocket. You need to wait for the first ready and authenticated websocket (use concat or other)')
                return just([])
            return response_messages.pipe(
                wait_for_response(
                    ws.value.send_message(
                        CryptodotcomRequestMessage(MethodName.GET_TRADES, params={
                            "instrument_name": instrument_name,
                            "count": count
                        })
                    ),
                    2.0
                ),
                operators.map(lambda x: [Trade(**d) for d in x.result['data']]),
            )
        return defer(get_trades_)
    return get_trades
