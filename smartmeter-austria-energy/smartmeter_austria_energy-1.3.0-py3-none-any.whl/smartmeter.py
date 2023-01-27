"""The Smartmeter definition."""

import asyncio
import binascii
import logging
import re
import threading
import time

import serial
from serial.serialutil import SerialException, SerialTimeoutException

from .decrypt import Decrypt
from .eventtypes import Event
from .exceptions import (
    SmartmeterException,
    SmartmeterSerialException,
    SmartmeterTimeoutException,
)
from .obisdata import ObisData, ObisDataEventArgs
from .supplier import SUPPLIERS


class Smartmeter():
    """Connects and reads data from the smartmeter."""
    def __init__(self,
                 supplier_name: str,
                 port: str,
                 key_hex_string : str,
                 interval : int = 1,
                 timeout : float = 0.2,
                 baudrate : int = 2400,
                 parity: str = serial.PARITY_NONE,
                 stopbits: str = serial.STOPBITS_ONE,
                 bytesize: str = serial.EIGHTBITS,
                 serial_read_chunk_size: int = 100) -> None:
        self._supplier_name = supplier_name
        self._port: str = port
        self._key_hex_string = key_hex_string
        self._baudrate : int = baudrate
        self._parity: str = parity
        self._stopbits: str = stopbits
        self._bytesize: str = bytesize
        self._interval: int = interval
        self._timeout: float = timeout
        self._serial_read_chunk_size : int = serial_read_chunk_size

        self._mySerial : serial = None
        self._obisData : ObisData = None
        self._obisdata_changed : Event = Event()
        self._read_thread : threading.Thread = None

        self._logger = logging.getLogger(__name__)
        self._is_running: bool = False
        self._ex: Exception = None

    @property
    def is_running(self) -> bool:
        return self._is_running

    @property
    def __obisData(self) -> ObisData:
        return self._obisData

    @__obisData.setter
    def __obisData(self, obisData):
        if (self._obisData != obisData):
            eventArgs = ObisDataEventArgs(obisData)
            if (self._obisdata_changed is not None):
                self._obisdata_changed.notify(sender=self, args=eventArgs)
            self._obisData = obisData

    @property
    def obisdata_changed(self) -> Event:
        return self._obisdata_changed

    @obisdata_changed.setter
    def obisdata_changed(self, obisdata_changed):
        self._obisdata_changed = obisdata_changed

    def close(self) -> None:
        self._is_running = False

    async def async_read_once(self) -> ObisData:
        self._ex = None
        self.__open_serial()
        self._is_running = self._mySerial.isOpen()

        supplier = SUPPLIERS.get(self._supplier_name)
        obisdata = await self.__async_read(supplier)
        self.__close_serial()
        return obisdata

    def start_reading(self) -> None:
        self._logger.debug("Try to start reading.")
        self._ex = None
        self._read_thread = threading.Thread(target=self.__start_read)
        self._read_thread.start()
        self._logger.debug("Reading started.")

    def stop_reading(self) -> None:
        self._logger.debug("Try to stop reading.")
        self._read_thread.join()
        self._is_running = False
        self.__close_serial()
        self._ex = None
        self._logger.debug("Reading stopped.")

    def __start_read(self) -> None:
        asyncio.run(self.__async_read_wrapper())

    async def __async_read_wrapper(self) -> None:
        try:
            await self.__async_read_loop()
        except Exception as ex:
            self._ex = ex
            self._is_running = False
            self.__close_serial()

    # read method was mainly taken from https://github.com/tirolerstefan/kaifa
    async def __async_read_loop(self) -> None:
        self.__open_serial()
        self._is_running = self._mySerial.isOpen()
        self._logger.debug("Start reading from serial.")

        supplier = SUPPLIERS.get(self._supplier_name)

        # outer loop
        while self._is_running:
            start = time.monotonic()

            obisdata = await self.__async_read(supplier)
            self.__obisData = obisdata

            end = time.monotonic()
            needed = end - start
            self._logger.debug(f"Needed {needed} s for OBIS data.")

            sleep_time = self._interval - needed
            if (sleep_time < 0):
                sleep_time = 0

            await asyncio.sleep(sleep_time)

        self.__close_serial()

    # read one pair of frames
    async def __async_read(self, supplier) -> ObisData:
        stream = b''      # filled by serial device
        frame1 = b''      # parsed telegram1
        frame2 = b''      # parsed telegram2

        frame1_start_pos = -1          # pos of start bytes of telegram 1 (in stream)
        frame2_start_pos = -1          # pos of start bytes of telegram 2 (in stream)

        start = time.monotonic()
        self._logger.debug("Fetch next frame.")

        # "telegram fetching loop" (as long as we have found two full telegrams)
        # frame1 = first telegram (68fafa68), frame2 = second telegram (68727268)
        while self._is_running:
            self._logger.debug("Read in chunks.")

            # Read in chunks. Each chunk will wait as long as specified by
            # serial timeout. As the meters we tested send data every 5s the
            # timeout must be <5. Lower timeouts make us fail quicker.
            byte_chunk = self._mySerial.read(size=self._serial_read_chunk_size)
            stream += byte_chunk
            frame1_start_pos = stream.find(supplier.frame1_start_bytes)
            frame2_start_pos = stream.find(supplier.frame2_start_bytes)

            # fail as early as possible if we find the segment is not complete yet.
            if((stream.find(supplier.frame1_start_bytes) < 0)
                    or (stream.find(supplier.frame2_start_bytes) <= 0)
                    or (stream[-1:] != supplier.frame2_end_bytes)
                    or (len(byte_chunk) == self._serial_read_chunk_size)):

                self._logger.debug("Segment is not complete yet.")
                stop = time.monotonic()
                elapsed = stop - start
                if (elapsed < 10):
                    await asyncio.sleep(0.5)
                    continue
                else:
                    raise SmartmeterTimeoutException()

            if (frame2_start_pos != -1):
                # frame2_start_pos could be smaller than frame1_start_pos
                if frame2_start_pos < frame1_start_pos:
                    # start over with the stream from frame1 pos
                    self._logger.debug("Start over with the stream from frame1 pos.")
                    stream = stream[frame1_start_pos:len(stream)]

                    continue

                # we have found at least two complete telegrams
                self._logger.debug("We have found at least two complete telegrams.")
                regex = binascii.unhexlify('28' + supplier.frame1_start_bytes_hex + '7c' + supplier.frame2_start_bytes_hex + '29')  # re = '(..|..)'
                my_list = re.split(regex, stream)
                my_list = list(filter(None, my_list))  # remove empty elements
                # l after split (here in following example in hex)
                # l = ['68fafa68', '53ff00...faecc16', '68727268', '53ff...3d16', '68fafa68', '53ff...d916', '68727268', '53ff.....']

                # take the first two matching telegrams
                for i, el in enumerate(my_list):
                    if el == supplier.frame1_start_bytes:
                        frame1 = my_list[i] + my_list[i + 1]
                        frame2 = my_list[i + 2] + my_list[i + 3]
                        break

                # check for weird result -> exit
                if (len(frame1) == 0) or (len(frame2) == 0):
                    self._logger.debug("Exit because of weird result.")
                    self.is_running = False

                break

        # If we are stopped do not parse.
        if (self._is_running):
            self._logger.debug("Next step is decrypting.")
            await asyncio.sleep(0)
            dec = Decrypt(supplier, frame1, frame2, self._key_hex_string)
            dec.parse_all()

            obisdata = ObisData(dec, supplier.supplied_values)

            end = time.monotonic()
            needed = end - start
            self._logger.debug(f"Needed {needed} s for OBIS data.")

            return obisdata
        return None

    def __open_serial(self) -> None:
        try:
            self._mySerial = serial.Serial(
                port=self._port,
                baudrate=self._baudrate,
                parity=self._parity,
                stopbits=self._stopbits,
                bytesize=self._bytesize,
                timeout=self._timeout)
        except SerialTimeoutException as ex:
            self._logger.debug("Timeout happened at closing.")
            raise SmartmeterTimeoutException(f"'{self._port}' has a timeout.") from ex
        except SerialException as ex:
            self._logger.debug("SerialException happened at closing.")
            raise SmartmeterSerialException(f"'{self._port}' cannot be opened.") from ex
        except Exception as ex:
            self._logger.debug("Exception happened at closing.")
            raise SmartmeterException(f"Connection to '{self._port}' failed.") from ex

    def __close_serial(self):
        try:
            self._mySerial.close()
        except Exception as ex:
            raise SmartmeterException(f"Closing port '{self._port}' failed.") from ex
