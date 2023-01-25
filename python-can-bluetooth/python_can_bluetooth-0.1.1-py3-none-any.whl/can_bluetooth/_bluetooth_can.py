# -*- coding: utf-8 -*-
"""
A simple text based interface loosely based on the 'serial' interface, with
amendments to the protocol to add error checking (using the same CRC algortihm
as the CAN physical layer)

See the interface documentation for the format being used.

Created on Wed Dec 28 20:56:33 2022

Copyright (C) 2023 Matt Woodhead
"""

import io
import logging
import string
import struct
import time
from typing import Any, List, Tuple, Optional

from can import BusABC, BusState, Message
from can import (
    CanError,
    CanInterfaceNotImplementedError,
    CanInitializationError,
    CanOperationError,
    CanTimeoutError,
)
from can.typechecking import AutoDetectedConfig

logger = logging.getLogger("can.bluetoothspp")

try:
    import serial
except ImportError:
    logger.warning(
        (
            "You won't be able to use the python-can-bluetooth backend without ",
            "the serial module installed!",
        )
    )
    serial = None

try:
    from serial.tools.list_ports import comports as list_comports
except ImportError:
    # If unavailable on some platform, just return nothing
    def list_comports() -> List[Any]:
        """
        A dummy function to cover the case where the list_comports method from the serial library is not available
        """
        return []


def list_bluetooth_ports() -> List[Any]:
    """
    A function to filter the COM ports on computer to those acting as Serial over Bluetooth (SPP) links
    :return: DESCRIPTION
    :rtype: List[Any]

    """
    ports = list_comports()
    if ports:
        ports = [p for p in ports if r"BTHENUM\{" in p.hwid]  # TODO: detection currently Windows only
        return ports
    return []


class BluetoothSPPBus(BusABC):
    """
    Enable basic can communication over a serial device.

    .. note:: See :meth:`~_recv_internal` for some special semantics.

    """

    def __init__(
        self,
        channel: str,
        bitrate: int = 250000,
        bt_baudrate: int = 921600,
        timeout: float = 0.1,
        state: int = BusState.PASSIVE,
        rtscts: bool = False,
        timestamps_use_computer_time: bool = True,
        *args,
        **kwargs,
    ) -> None:
        """
        :param channel:
            The serial port to open. For example "/dev/ttyS1" or
            "/dev/ttyUSB0" on Linux or "COM1" on Windows systems.
            This should be the 'Outgoing' port of the bluetooth SPP com port pair.

        :param bitrate:
            Bit rate of the BT CAN interface in bit/s (default 250000).

        :param baudrate:
            Baud rate of the Bluetooth SPP port in bit/s (default 921600).

        :param timeout:
            Timeout for the serial device in seconds (default 0.1).

        :param rtscts:
            turn hardware handshake (RTS/CTS) on and off

        :param timestamps_use_computer_time:
            enable/disbale the adjustment of the timestamp values to match the
            computers time (useful when datalogging and trying to establish
            event timings)

        :raises ~can.exceptions.CanInitializationError:
            If the given parameters are invalid.
        :raises ~can.exceptions.CanInterfaceNotImplementedError:
            If the serial module is not installed.
        """

        if not serial:
            raise CanInterfaceNotImplementedError("the serial module is not installed")

        if not channel:
            raise TypeError("Must specify a serial port.")

        self.channel_info = f"Serial interface: {channel}"

        try:
            self._ser = serial.serial_for_url(channel, baudrate=bt_baudrate, timeout=timeout, rtscts=rtscts)
        except ValueError as error:
            raise CanInitializationError("could not create the serial device") from error

        if timestamps_use_computer_time:
            self._bus_pc_start_time_s = round(time.time(), 4)
        else:
            self._bus_pc_start_time_s = 0

        # interface configuration attributes
        # if these are changed after initialisation, self._send_interface_can_config() must be called
        self.bitrate = bitrate  # CAN Bit rate
        self.state = state  # 0 = Active, 1 = passive, 2 = error
        self.interface_enable_can = True  # Enable/disable can interface

        super().__init__(channel, *args, **kwargs)

    def shutdown(self) -> None:
        """
        Close the serial interface.
        """
        super().shutdown()
        self._ser.close()

    def send(self, msg: Message, timeout: Optional[float] = None, interface_control: Optional[bool] = False) -> None:
        """
        Send a message over the serial device.

        :param msg:
            Message to send.

            .. note:: Flags like ``extended_id``, ``is_remote_frame`` and
                      ``is_error_frame`` will be ignored.

            .. note:: If the timestamp is a float value it will be converted
                      to an integer.

        :param timeout:
            This parameter will be ignored. The timeout value of the channel is
            used instead.

        :param interface_control:
            This boolean determines if the message is a CAN message or an interface control message (the difference
            being the start and termination bytes of the message stream to allow the interface to distinguish between
            the different types of data)

        """
        # Pack timestamp
        try:
            timestamp = struct.pack(">I", int(msg.timestamp * 1000))
        except struct.error as ste:
            raise ValueError("Timestamp is out of range") from ste

        # Pack arbitration ID
        try:
            arbitration_id = struct.pack(">I", msg.arbitration_id)
        except struct.error as ste:
            raise ValueError("Arbitration ID is out of range") from ste

        # pack flags
        try:
            flag_byte = (1 * msg.is_extended_id) + (2 * msg.is_error_frame) + (4 * msg.is_remote_frame)
            flag_byte = struct.pack("<B", flag_byte)
        except struct.error as ste:
            raise ValueError("Invalid flag setting") from ste

        # prepare variables for message construction
        byte_msg_core = bytearray()
        byte_msg = bytearray()

        # Assemble core message (for CRC calculation)
        byte_msg_core.append(msg.dlc)
        byte_msg_core += flag_byte
        byte_msg_core += arbitration_id
        byte_msg_core += msg.data

        # CRC is calculated on the DLC, flags, ID, and Data bytes
        print(f"CRC: {calculate_crc15(byte_msg_core)}")
        byte_msg_core += struct.pack("<H", calculate_crc15(byte_msg_core))

        # prepend start byte and timestamp to the main message bytearray
        if interface_control:
            byte_msg.append(0xCC)  # interface control message
        else:
            byte_msg.append(0xAA)  # CAN message
        byte_msg += timestamp

        # combine the byte arrays into the final message array
        byte_msg += byte_msg_core
        if interface_control:
            byte_msg.append(0xDD)  # interface control message
        else:
            byte_msg.append(0xBB)  # CAN message
        # <AA><Time 0><Time 1><Time 2><Time 3><DLC><Flags><ID 0><ID 1><ID 2><ID 3><Data 0>...<CRC 0><CRC 1><BB>

        # Write to serial device
        try:
            print(byte_msg.hex())
            self._ser.write(byte_msg)
        except serial.PortNotOpenError as error:
            raise CanOperationError("writing to closed port") from error
        except serial.SerialTimeoutException as error:
            raise CanTimeoutError() from error

    def _recv_internal(self, timeout: Optional[float]) -> Tuple[Optional[Message], bool]:
        """
        Read a message from the serial device.

        :param timeout:

            .. warning::
                This parameter will be ignored. The timeout value of the channel is used.

        :returns:
            Received message and :obj:`False` (because no filtering has taken place).
        """
        try:
            rx_byte = self._ser.read()
            if rx_byte:
                can_start_byte = ord(rx_byte) == 0xAA
                interface_start_byte = ord(rx_byte) == 0xCC
            else:
                return None, False

            if can_start_byte or interface_start_byte:
                crc_byte_array = bytearray()  # create a bytearray to store data for CRC

                # read in timestamp bytes
                timestamp_byte = self._ser.read(4)
                timestamp = struct.unpack("<I", timestamp_byte)[0]

                # read in DLC byte
                dlc_byte = self._ser.read()
                try:
                    dlc = ord(dlc_byte)
                except TypeError:
                    dlc = 0
                if dlc > 8:
                    raise ValueError("received DLC may not exceed 8 bytes")
                crc_byte_array += dlc_byte

                # read in flag byte
                flag_byte = ord(self._ser.read())
                is_extended_id = (flag_byte & 1) == 1
                is_error_frame = (flag_byte & 2) == 1
                is_remote_frame = (flag_byte & 4) == 1
                crc_byte_array.append(flag_byte)

                # read in arbitration id
                id_bytes = self._ser.read(4)
                arbitration_id = struct.unpack("<I", id_bytes)[0]
                if arbitration_id >= 0x20000000:
                    raise ValueError("received arbitration id may not exceed 2^29 (0x20000000)")
                crc_byte_array += id_bytes

                # read in data bytes
                data = self._ser.read(dlc)  # read as many bytes as the DLC stated there were
                crc_byte_array += data

                ser = self._ser.read(2)
                sent_crc = struct.unpack("<H", ser)[0]

                # CRC is calculated on the DLC, flags, ID, and Data bytes
                calc_crc = calculate_crc15(crc_byte_array)
                if sent_crc != calc_crc:
                    raise BusCRCError(
                        f"The message CRC (0x{sent_crc:02x}) and calculated CRC (0x{calc_crc:02x}) don't match"
                    )

                delimiter_byte = ord(self._ser.read())
                if can_start_byte and delimiter_byte == 0xBB:
                    # received message data okay
                    msg = Message(
                        # TODO: We are only guessing that they are milliseconds
                        timestamp=self._bus_pc_start_time_s + (timestamp / 1000),
                        arbitration_id=arbitration_id,
                        dlc=dlc,
                        data=data,
                        is_extended_id=is_extended_id,
                        is_error_frame=is_error_frame,
                        is_remote_frame=is_remote_frame,
                    )
                    return msg, False
                if interface_start_byte and delimiter_byte == 0xDD:
                    # received message data okay
                    msg = Message(
                        # TODO: We are only guessing that they are milliseconds
                        timestamp=self._bus_pc_start_time_s + (timestamp / 1000),
                        arbitration_id=arbitration_id,
                        dlc=dlc,
                        data=data,
                        is_extended_id=is_extended_id,
                        is_error_frame=is_error_frame,
                        is_remote_frame=is_remote_frame,
                    )
                    return self._process_interface_msg(msg)
                else:
                    # TODO: do we actually want to raise the below exception, or just return 'None, False'?
                    raise CanOperationError(f"invalid delimiter byte while reading message: {delimiter_byte:02x}")
            else:
                return None, False

        except serial.SerialException as error:
            raise CanOperationError("could not read from serial") from error

    def fileno(self) -> int:
        try:
            return self._ser.fileno()
        except io.UnsupportedOperation as ioe:
            raise NotImplementedError("fileno is not implemented using current CAN bus on this platform") from ioe
        except Exception as exception:
            raise CanOperationError("Cannot fetch fileno") from exception

    @staticmethod
    def _detect_available_configs() -> List[AutoDetectedConfig]:
        return [{"interface": "bluetooth", "channel": port.device} for port in list_bluetooth_ports()]

    def _process_interface_msg(self, message_obj: Message = None) -> Tuple[Optional[Message], bool]:
        """
        This private function processes any messages from the interface board. Generally these are responses to
        confiuration requests or IO statuses for some implementations of the bluetooth interface.
        """
        print("Received interface message:", message_obj)
        pass  # TODO

    def set_device_bt_name(self, name: str = "") -> bool:

        if not isinstance(name, str):
            return False
        name.strip()
        if not name:
            return False

        allowed_chars = set(string.ascii_letters + string.digits + "_-")
        if set(name) - allowed_chars:  # if the name contains characters that arent allowed
            # TODO raise exception
            return False

        string_chunk_len = 7  # 7 bytes - the eighth is used as a message counter (i.e. message)
        string_chunks = [name[i : i + string_chunk_len] for i in range(0, len(name), string_chunk_len)]
        number_of_chunks = len(string_chunks)

        if len(string_chunks) > 0xF:
            print("The bluetooth name cannot be more than 35 characters")
            # TODO: raise exception
            return False

        for i, chunk in enumerate(string_chunks):
            config_msg = Message(arbitration_id=0x002, is_extended_id=False)
            # bits 0-3 are the message number, 4-7 is the total number of messages
            config_msg.data += i + (number_of_chunks << 4)
            config_msg.data += chunk.encode("ASCII")
            self.send(config_msg, interface_control=True)

        return True

    def _send_interface_can_config(self) -> bool:
        """
        This private function sends the values of the class configuration attributes to the BT interface
        """

        config_msg = Message(arbitration_id=0x001, is_extended_id=False)
        if self.interface_enable_can:  # if the bus is enabled when the update function is called
            if self.state == BusState.ACTIVE:
                config_bits = (1 << 1) + int(self.interface_enable_can)
            else:
                config_bits = (0 << 1) + int(self.interface_enable_can)
            config_msg.data += struct.pack(">B", config_bits)
            config_msg.data += struct.pack(">I", int(self.bitrate))
        else:
            config_msg.data += bytearray((0, 0, 0, 0, 0))  # otherwise disable CAN on the interface

        self.send(config_msg, interface_control=True)


def calculate_crc15(byte_array: bytearray = None):
    """
    A function that calculates the CRC value for a python-can Message object using the DLC, flags, ID, and Data bytes

    :param byte_array:
        Expects a byte_array (length not specified).
        .. warning::
            There is no type checking in this function as it is only intended
            for internal use in the can-bluetooth module.

    :returns:
        Received integer number from CRC calculation
    """

    last_crc_value = 0x0000
    can_crc15_polynomial = 0xC599

    def next_crc15_value(data):
        # 1100010110011001  - P(x) = x^15 + x^14 + x^10 + x^8 + x^7 + x^4 + x^3 + x^0
        nonlocal last_crc_value
        last_crc_value ^= data << 7

        for _ in range(8):
            last_crc_value <<= 1
            if last_crc_value & 0x8000:
                last_crc_value ^= can_crc15_polynomial

        return last_crc_value & 0x7FFF

    for byte in byte_array:
        next_crc15_value(byte)

    return last_crc_value


class BusCRCError(CanError):
    """Indicates an error in the network transmission of the :class:`can.Message`.

    This is because the CRC value sent in the message and the calculated CRC value
    for the frame contents do not match.

    Example scenarios:
      - The transmitting node has calculated the CRC value incorrectly
      - The data has been corrupted during transmission
      - The data has been corrupted during reading the messages from the serial port
    """
