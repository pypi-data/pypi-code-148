"""
Test for Bluetooth Interface
"""


import unittest
from unittest.mock import patch
from time import time

import can
from can.exceptions import CanOperationError, CanInitializationError, CanTimeoutError

# from can.interfaces.serial.serial_can import SerialBus
from can_bluetooth import BluetoothSPPBus, BusCRCError
from .test_setup import SerialDummy, ComparingMessagesTestCase, TIMEOUT


class SimpleSerialTestBase(ComparingMessagesTestCase):

    MAX_TIMESTAMP = 0xFFFFFFFF / 1000

    def __init__(self):
        ComparingMessagesTestCase.__init__(self, allowed_timestamp_delta=None, preserves_channel=True)

    # def test_serial_module_missing(self):  # TODO - get check for missing serial module working
    #     """
    #     tests the behaviour when the serial module is not installed
    #     """
    #     def _import_test():
    #         with patch.dict('sys.modules', {'serial': None}):
    #             from can_bluetooth import _bluetooth_can
    #             del _bluetooth_can

    #     self.assertRaises(ModuleNotFoundError, _import_test)

    def test_list_comports(self):
        """
        tests the behaviour when the serial module is not installed
        """
        ports = self.bus._detect_available_configs()  # TODO - change this to use the python-can entry point
        self.assertIsInstance(ports, list)

    def test_rx_tx_min_max_data(self):
        """
        Tests the transfer from 0x00 to 0xFF for a 1 byte payload
        """
        for b in range(0, 255):
            msg = can.Message(data=[b])
            self.bus.send(msg)
            msg_receive = self.bus.recv()
            self.assertMessageEqual(msg, msg_receive)

    def test_rx_tx_min_max_dlc(self):
        """
        Tests the transfer from a 1 - 8 byte payload
        """
        payload = bytearray()
        for _ in range(1, 9):
            payload.append(0)
            msg = can.Message(data=payload)
            self.bus.send(msg)
            msg_receive = self.bus.recv()
            self.assertMessageEqual(msg, msg_receive)

    def test_rx_tx_data_none(self):
        """
        Tests the transfer without payload
        """
        msg = can.Message(data=None)
        self.bus.send(msg)
        msg_receive = self.bus.recv()
        self.assertMessageEqual(msg, msg_receive)

    def test_rx_tx_min_id(self):
        """
        Tests the transfer with the lowest arbitration id
        """
        msg = can.Message(arbitration_id=0)
        self.bus.send(msg)
        msg_receive = self.bus.recv()
        self.assertMessageEqual(msg, msg_receive)

    def test_rx_tx_max_id(self):
        """
        Tests the transfer with the highest arbitration id
        """
        msg = can.Message(arbitration_id=536870911)
        self.bus.send(msg)
        msg_receive = self.bus.recv()
        self.assertMessageEqual(msg, msg_receive)

    def test_rx_tx_max_timestamp(self):
        """
        Tests the transfer with the highest possible timestamp
        """

        msg = can.Message(timestamp=self.MAX_TIMESTAMP)
        self.bus.send(msg)
        msg_receive = self.bus.recv()
        self.assertMessageEqual(msg, msg_receive)
        self.assertEqual(msg.timestamp, msg_receive.timestamp)

    def test_rx_tx_max_timestamp_error(self):
        """
        Tests for an exception with an out of range timestamp (max + 1)
        """
        msg = can.Message(timestamp=self.MAX_TIMESTAMP + 1)
        self.assertRaises(ValueError, self.bus.send, msg)

    def test_rx_tx_min_timestamp(self):
        """
        Tests the transfer with the lowest possible timestamp
        """
        msg = can.Message(timestamp=0)
        self.bus.send(msg)
        msg_receive = self.bus.recv()
        self.assertMessageEqual(msg, msg_receive)
        self.assertEqual(msg.timestamp, msg_receive.timestamp)

    def test_rx_tx_min_timestamp_error(self):
        """
        Tests for an exception with an out of range timestamp (min - 1)
        """
        msg = can.Message(timestamp=-1)
        self.assertRaises(ValueError, self.bus.send, msg)

    def test_rx_tx_computer_timestamp(self):
        """
        Tests for the timestamps being reported relative to the computers time
        """
        # change the bus to use the computer timestamps
        self.bus.timestamps_use_computer_time = True
        self.bus._bus_pc_start_time_s = round(time(), 4)

        # send a message to the test bus
        msg = can.Message(timestamp=0)  # timestamp not relevant - we are testing the receive timestamps
        self.bus.send(msg)

        receive_time = round(time(), 1)  # round to 1dp to prevent likeyhood of the timestamps being too different
        msg_receive = self.bus.recv()
        self.assertEqual(receive_time, round(msg_receive.timestamp, 1))

        # set the bus back to not using the computer timestamps
        self.bus.timestamps_use_computer_time = False
        self.bus._bus_pc_start_time_s = 0

    def test_when_no_fileno(self):
        """
        Tests for the fileno method catching the missing pyserial implementeation on the Windows platform
        """
        try:
            fileno = self.bus.fileno()
        except NotImplementedError:
            pass  # allow it to be left non-implemented for Windows platform
        else:
            fileno.__gt__ = (
                lambda self, compare: True
            )  # Current platform implements fileno, so get the mock to respond to a greater than comparison
            self.assertIsNotNone(fileno)
            self.assertFalse(fileno == -1)
            self.assertTrue(fileno > 0)


class SimpleSerialTest(unittest.TestCase, SimpleSerialTestBase):
    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        SimpleSerialTestBase.__init__(self)

    def setUp(self):
        self.patcher = patch("serial.Serial")
        self.mock_serial = self.patcher.start()
        self.serial_dummy = SerialDummy()
        self.mock_serial.return_value.write = self.serial_dummy.write
        self.mock_serial.return_value.read = self.serial_dummy.read
        self.addCleanup(self.patcher.stop)
        self.bus = BluetoothSPPBus("bus", timeout=TIMEOUT, timestamps_use_computer_time=False)

    def tearDown(self):
        self.serial_dummy.reset()


class SimpleSerialLoopTest(unittest.TestCase, SimpleSerialTestBase):
    def __init__(self, *args, **kwargs):
        unittest.TestCase.__init__(self, *args, **kwargs)
        SimpleSerialTestBase.__init__(self)

    def setUp(self):
        self.bus = BluetoothSPPBus("loop://", timeout=TIMEOUT, timestamps_use_computer_time=False)

    def tearDown(self):
        self.bus.shutdown()


crc_inputs_and_results = (
    (bytearray([0xFF]), 0x5F90),
    (bytearray([0x00]), 0x0000),
    (bytearray([0x01]), 0x4599),
    (bytearray([0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA]), 0x07FB),
    (bytearray([0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37]), 0x5F90),
    (bytearray([0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]), 0x66CA),
)

if __name__ == "__main__":
    unittest.main()
