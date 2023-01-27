"""Wall Pad Socket Client"""
import asyncio
import logging
import time
from dataclasses import dataclass
from typing import Any

_CONNECTION_DEFAULT_TIMEOUT = 5.0
_READ_DEFAULT_TIMEOUT = 5.0
_READ_BUFFER_DEFAULT_SIZE = 512  # 512 bytes
_QUEUE_WAIT_DEFAULT_TIMEOUT = 1.0
_RECEIVE_PACKET_DEFAULT_INTERVAL = 0.3
_SEND_PACKET_DEFAULT_INTERVAL = 0.4
_SEND_PACKET_RETRY_DEFAULT_COUNT = 5

_LOGGER = logging.getLogger(__name__)


class _WpSendData:
    """Socket send data"""

    def __init__(self, packet: bytes):
        self._complete = asyncio.Event()
        self._try_cnt = 0
        self._result = False
        self.packet = packet

    def inc_try(self) -> int:
        """Socket send try"""
        self._try_cnt += 1
        return self._try_cnt

    def set(self, result: bool) -> None:
        """Socket send result"""
        self._result = result

        if not self._complete.is_set():
            self._complete.set()

    async def wait(self) -> bool:
        """Socket send wait"""
        await self._complete.wait()
        return self._result


@dataclass
class WpSocketConfig:
    """Wall Pad Socket Config"""
    connection_timeout: float
    read_timeout: float
    read_buffer_size: int
    queue_wait_timeout: float
    receive_packet_interval: float
    send_packet_interval: float
    send_packet_retry_count: int


class WpSocketClient:
    """Wall Pad Socket Client"""
    _reader: asyncio.StreamReader
    _writer: asyncio.StreamWriter

    def __init__(self, host: str, port: int, async_packets_handler, **kwds):
        self.host = host
        self.port = port
        self._async_receive_handler = async_packets_handler
        self._config = WpSocketConfig(
            kwds.pop('connection_timeout', _CONNECTION_DEFAULT_TIMEOUT),
            kwds.pop('read_timeout', _READ_DEFAULT_TIMEOUT),
            kwds.pop('read_buffer_size', _READ_BUFFER_DEFAULT_SIZE),
            kwds.pop('queue_wait_timeout', _QUEUE_WAIT_DEFAULT_TIMEOUT),
            kwds.pop('receive_packet_interval', _RECEIVE_PACKET_DEFAULT_INTERVAL),
            kwds.pop('send_packet_interval', _SEND_PACKET_DEFAULT_INTERVAL),
            kwds.pop('send_packet_retry_count', _SEND_PACKET_RETRY_DEFAULT_COUNT)
        )

        self._wait_tasks: Any = None
        self._loop = asyncio.get_event_loop()
        self._receive_packet_queue: asyncio.Queue[bytes] = asyncio.Queue()
        self._send_packet_queue: asyncio.Queue[_WpSendData] = asyncio.Queue()

        self._connect_retry_cnt = 0
        self.connected = False
        self._last_receive_time = time.time()
        self._last_send_time = time.time()

    async def async_on_connected(self):
        """Socket connected notifications"""

    async def async_on_disconnected(self):
        """Socket disconnected notifications"""

    async def async_on_reconnect(self):
        """Socket reconnect notifications"""

    async def async_connect(self) -> bool:
        """Socket connect"""
        await self._async_wait_for_disconnect()

        _LOGGER.debug('connecting to server %s', self.host)
        try:
            asyncio.set_event_loop(self._loop)
            self._reader, self._writer = await asyncio.wait_for(
                asyncio.open_connection(self.host, self.port),
                timeout=self._config.connection_timeout)
            self.connected = True
            self._connect_retry_cnt = 0

            self._loop.create_task(self.async_on_connected())

            tasks = [self._loop.create_task(self._async_reader_handler()),
                     self._loop.create_task(self._async_reader()),
                     self._loop.create_task(self._async_writer())]
            self._wait_tasks = asyncio.wait(tasks)
            return True
        except Exception as ex:
            _LOGGER.error("connection error, %s, %s", self.host, ex)
            self.disconnect()
        return False

    async def _async_reconnect(self):
        """Socket reconnect"""
        self._loop.create_task(self.async_on_reconnect())
        wait_time = self._connect_retry_cnt * 5 if self._connect_retry_cnt < 12 else 60
        _LOGGER.debug('reconnect connect, wait %d s', wait_time)
        await asyncio.sleep(wait_time)
        self._connect_retry_cnt += 1
        if not await self.async_connect():
            await self._async_reconnect()

    async def async_send_packet(self, packet: bytes) -> bool:
        """Send packet"""
        send_data = _WpSendData(packet)
        await self._send_packet_queue.put(send_data)
        return await send_data.wait()

    async def _async_reader_handler(self):
        """Queue read handler"""
        _LOGGER.debug('message handler start')
        while self.connected:
            try:
                packets = await asyncio.wait_for(self._receive_packet_queue.get(),
                                                 timeout=self._config.queue_wait_timeout)
                await self._async_receive_handler(packets)
                self._receive_packet_queue.task_done()
            except asyncio.TimeoutError:
                continue
            except Exception as ex:
                _LOGGER.error('message handler error, %s', ex)

        _LOGGER.debug('message handler end')

    async def _async_reader(self):
        """Socket read packet"""
        _LOGGER.debug('reader start')
        while self.connected:
            try:
                if (data := await asyncio.wait_for(self._reader.read(self._config.read_buffer_size),
                                                   timeout=self._config.read_timeout)) is None:
                    self._loop.create_task(self._async_reconnect())
                    break
                self._last_receive_time = time.time()

                _LOGGER.debug('Received [%d]: %s', len(data), data.hex())
                await self._receive_packet_queue.put(data)
            except Exception as ex:
                _LOGGER.error('reader error, %s', ex)
                self._loop.create_task(self._async_reconnect())
                break
        _LOGGER.debug('reader end')

    async def _async_writer(self):
        """Socket write packet"""
        _LOGGER.debug('writer start')
        while self.connected:
            try:
                send_data: _WpSendData \
                    = await asyncio.wait_for(self._send_packet_queue.get(),
                                             timeout=self._config.queue_wait_timeout)
                while True:
                    now = time.time()
                    send_interval = now - self._last_send_time
                    receive_interval = now - self._last_receive_time
                    if send_interval > self._config.receive_packet_interval \
                            and receive_interval > self._config.send_packet_interval:
                        self._writer.write(send_data.packet)
                        await self._writer.drain()
                        self._last_send_time = time.time()
                        _LOGGER.debug('Send: %s', send_data.packet.hex())
                        send_data.set(True)
                        self._send_packet_queue.task_done()
                        break

                    if send_data.inc_try() > self._config.send_packet_retry_count:
                        _LOGGER.warning('Send fail: %s', send_data.packet.hex())
                        send_data.set(False)
                        break

                    if send_interval > receive_interval:
                        delay = self._config.receive_packet_interval - receive_interval
                        _LOGGER.info('Send, wait receive interval : %f', delay)
                        await asyncio.sleep(delay)
                    else:
                        delay = self._config.send_packet_interval - send_interval
                        _LOGGER.info('Send, wait send interval: %f', delay)
                        await asyncio.sleep(delay)

            except asyncio.TimeoutError:
                continue
            except Exception as ex:
                _LOGGER.error('writer error, %s', ex)
                self._loop.create_task(self._async_reconnect())
                break
        _LOGGER.debug('writer end')

    async def _async_wait_for_disconnect(self):
        """disconnect and task exit wait"""
        self.disconnect()
        if self._wait_tasks is None:
            return
        await self._wait_tasks
        self._wait_tasks = None

    def disconnect(self):
        """disconnect"""
        if not self.connected:
            return
        self.connected = False
        if not self._loop.is_closed():
            self._writer.close()
        self._loop.create_task(self.async_on_disconnected())

    def __del__(self):
        self.disconnect()
