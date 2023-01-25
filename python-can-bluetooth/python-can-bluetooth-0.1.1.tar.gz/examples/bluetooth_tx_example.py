# -*- coding: utf-8 -*-
"""
Created on Sat Dec 31 17:05:59 2022

bluetooth_tx_example.py

python-can-bluetooth
"""

import struct
import can
from can import Message
from threading import Timer
from time import ctime
from can_bluetooth import BluetoothSPPBus

DONE = False


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


# with can.Bus(interface="bluetooth", channel="COM5", bitrate=250000, echo=False) as bus:
with BluetoothSPPBus(channel="COM5", bitrate=500000, echo=False) as bus:

    def timeout():
        global DONE
        DONE = True

    msg = Message(
        timestamp=0.250,
        arbitration_id=0x1F0ABC,
        is_extended_id=True,
        data=[0xDE, 0xAD, 0xBE, 0xEF, 0xDE, 0xAD, 0xBE, 0xEF],
    )

    task = bus.send_periodic(msg, 0.1)
    t = Timer(15, timeout)
    t.start()
    print(f"TX started: {ctime()}")

    while not DONE:
        pass
    else:
        task.stop()
        print(f"TX Done: {ctime()}")
