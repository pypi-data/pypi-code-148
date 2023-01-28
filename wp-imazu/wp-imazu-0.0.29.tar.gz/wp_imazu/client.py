"""Wall Pad Imazu Socket Client"""
import asyncio
import logging
from collections import defaultdict
from typing import Optional

from wp_socket.client import WpSocketClient

from wp_imazu.packet import parse_packet

_LOGGER = logging.getLogger(__name__)

_PACKET_HEADER = b'\xf7'
_PACKET_TAIL = b'\xee'
_SEND_RETRY_DEFAULT_COUNT = 3
_RESPONSE_DEFAULT_TIMEOUT = 1.5


def checksum(packet: bytes) -> bool:
    """Imazu packet checksum"""
    if len(packet) == 0 or len(packet) != packet[1]:
        return False
    p_sum = 0
    for i in range(0, len(packet) - 2):
        p_sum ^= packet[i]
    return packet[len(packet) - 2] == p_sum


def makesum(packet: bytes) -> Optional[int]:
    """Imazu packet make checksum"""
    if len(packet) < packet[1] - 2:
        return None
    p_sum = 0
    for i in range(0, len(packet) - 2):
        p_sum ^= packet[i]
    return p_sum


class _ImazuPacketData:
    """Packet data"""

    def __init__(self):
        self._complete = asyncio.Event()
        self._try_cnt = 0

    def inc_try(self) -> int:
        """Packet send try"""
        self._try_cnt += 1
        return self._try_cnt

    def set(self):
        """Packet send event set"""
        self._try_cnt = 0
        if not self._complete.is_set():
            self._complete.set()

    def clear(self):
        """Packet send event clear"""
        self.set()
        self._complete.clear()

    async def wait(self) -> None:
        """Packet send wait"""
        await self._complete.wait()


class ImazuClient(WpSocketClient):
    """Wall Pad Imazu Socket Client"""

    def __init__(self, host: str, port: int, async_packet_handler, **kwds):
        super().__init__(host, port, self._async_packets_handler, **kwds)
        self._async_packet_handler = async_packet_handler
        self._packets: dict[str, _ImazuPacketData] = defaultdict(_ImazuPacketData)
        self._prev_packets: bytes = bytes()
        self._send_retry_cnt = kwds.pop('send_retry_count', _SEND_RETRY_DEFAULT_COUNT)
        self._response_timeout = kwds.pop('response_timeout', _RESPONSE_DEFAULT_TIMEOUT)

    async def async_on_connected(self):
        """Socket connected notifications"""
        _LOGGER.debug('connected')

    async def async_send(self, packet: bytes):
        """Socket write imazu packet"""
        data = bytearray(_PACKET_HEADER)
        data.append(0)  # len
        data.extend(packet)  # 01 or 1a, device, cmd, value_type, sub, change_value, state_value
        data.append(0)  # checksum
        data.extend(_PACKET_TAIL)
        data[1] = len(data)  # len

        # checksum
        if (_makesum := makesum(data)) is None:
            _LOGGER.warning('send invalid makesum: %s', data.hex())
            return
        data[-2] = _makesum

        if not checksum(data):
            _LOGGER.warning('send invalid checksum: %s', data.hex())
            return

        packet_id = f'{packet[1]:02x}_{packet[4]:02x}'
        packet_data = self._packets[packet_id]
        packet_data.clear()

        while packet_data.inc_try() <= self._send_retry_cnt:
            result = await super().async_send_packet(data)
            if not result:
                continue
            try:
                await asyncio.wait_for(packet_data.wait(),
                                       timeout=self._response_timeout)
                return
            except asyncio.TimeoutError:
                continue
            except Exception as ex:
                _LOGGER.error('send error, %s', ex)

        _LOGGER.warning('send retry fail')

    async def _async_packets_handler(self, packets: bytes):
        """Queue imazu packet handler"""
        packet_list = self._parse_packets(packets)
        for packet in packet_list:
            try:
                if not checksum(packet):
                    _LOGGER.warning('receive invalid checksum: %s', packet.hex())
                    continue
                imazu_packets = parse_packet(packet.hex())
                for imazu_packet in imazu_packets:
                    _LOGGER.debug(imazu_packet.description())
                    self._packets[imazu_packet.packet_id].set()
                    await self._async_packet_handler(imazu_packet)

            except Exception as ex:
                _LOGGER.error('packets handler error, %s, %s', ex, packet.hex())

    def _parse_packets(self, packets: bytes):
        """Queue imazu packet parse"""
        packet_list = []
        if self._prev_packets:
            packets = self._prev_packets + packets
            self._prev_packets = bytes()

        while packets:
            if (end_idx := packets.find(_PACKET_TAIL)) == -1:
                self._prev_packets = packets
                break
            if (start_idx := packets.rfind(_PACKET_HEADER, 0, end_idx)) == -1:
                _LOGGER.warning('parse unknown start packet, %s', packets[:end_idx + 1].hex())
                packets = packets[end_idx + 1:]
                continue
            if start_idx != 0:
                _LOGGER.warning('parse invalid start index, %s', packets[:start_idx].hex())

            packet_list.append(packets[start_idx: end_idx + 1])
            packets = packets[end_idx + 1:]
        return packet_list
