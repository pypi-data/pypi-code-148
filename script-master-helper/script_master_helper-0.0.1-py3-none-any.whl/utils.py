import asyncio
import datetime as dt
from asyncio import ProactorEventLoop
from typing import Optional, Union

import pendulum
from uvicorn import Server


def normalize_datetime(value: Union[dt.datetime, str, None]) -> Optional[pendulum.DateTime]:
    if not isinstance(value, pendulum.DateTime) and isinstance(value, dt.datetime):
        value = pendulum.instance(value).astimezone(pendulum.UTC)

    elif isinstance(value, str):
        value = pendulum.parse(value).astimezone(pendulum.UTC)

    return value


def custom_encoder(obj):
    if isinstance(obj, (pendulum.Date, pendulum.DateTime)):
        return obj.isoformat()

    raise TypeError(f"EncodeError: '{obj}' of type '{type(obj)}'")


class ProactorServer(Server):
    """https://stackoverflow.com/questions/70568070/running-an-asyncio-subprocess-in-fastapi-results-in-notimplementederror"""

    def run(self, sockets=None):
        loop = ProactorEventLoop()
        asyncio.set_event_loop(loop)  # since this is the default in Python 3.10, explicit selection can also be omitted
        asyncio.run(self.serve(sockets=sockets))
