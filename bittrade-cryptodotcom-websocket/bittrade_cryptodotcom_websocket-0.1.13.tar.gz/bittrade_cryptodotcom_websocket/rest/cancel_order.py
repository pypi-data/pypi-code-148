from typing import Any, Callable, Optional
from ..connection import wait_for_response
from ..models import (
    CryptodotcomResponseMessage,
    CryptodotcomRequestMessage,
    EnhancedWebsocketBehaviorSubject,
)
from reactivex import Observable, operators, disposable, just, throw
from ..events import MethodName
from reactivex.scheduler import NewThreadScheduler


def order_confirmation(
    messages: Observable[CryptodotcomResponseMessage],
    order_id: str,
):
    def is_match(message: CryptodotcomResponseMessage) -> bool:
        try:
            data = message.result["data"][0]
            return data["order_id"] == order_id and data["status"] == "canceled"
        except:
            return False

    return messages.pipe(
        operators.filter(is_match),
        operators.take(1),
        operators.timeout(2.0),
    )


def cancel_order_factory(
    messages: Observable[CryptodotcomResponseMessage],
    socket: EnhancedWebsocketBehaviorSubject,
) -> Callable[[str, bool | None, bool | None], Observable[bool]]:
    """Factory for cancel order API call

    Args:
        messages (Observable[CryptodotcomResponseMessage]): All messages
        socket (EnhancedWebsocketBehaviorSubject): Socket behavior subject

    Returns:
        Callable[ [str], Observable[bool] ]:

        order_id: str,

    """

    def cancel_order(order_id: str, wait_for_confirmation=True, ignore_errors=True):
        request = {"order_id": order_id}

        def subscribe(observer, scheduler=None):
            ws = socket.value
            recorded_messages = messages.pipe(
                operators.replay(),
            )
            sub = recorded_messages.connect(scheduler=NewThreadScheduler())

            def on_cancel(x):
                if x.code != 0 and not ignore_errors:
                    return throw(x.message)
                return just(x.result)

            send_request = messages.pipe(
                wait_for_response(
                    ws.send_message(
                        CryptodotcomRequestMessage(
                            MethodName.CANCEL_ORDER, params=request
                        )
                    ),
                    2.0,
                )
            )
            if wait_for_confirmation:
                successful_request = send_request.pipe(
                    operators.flat_map(on_cancel),
                    operators.flat_map(
                        lambda x: order_confirmation(recorded_messages, order_id)
                    ),
                    operators.catch(
                        lambda exc, _source: just(False)
                        if ignore_errors
                        else throw(exc)
                    ),
                )
            else:
                successful_request = send_request.pipe(operators.map(lambda _: True))

            return disposable.CompositeDisposable(
                sub,
                successful_request.subscribe(observer, scheduler=scheduler),
            )

        return Observable(subscribe)

    return cancel_order
