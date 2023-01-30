import unittest

from gfxinfo import SUPPORTED_GPU_DBS, PCIDevice


class DatabaseTests(unittest.TestCase):
    def test_check_db(self):
        for gpu_db in SUPPORTED_GPU_DBS:
            with self.subTest(GPU_DB=type(gpu_db).__name__):
                assert gpu_db.check_db()


class PCIDeviceTests(unittest.TestCase):
    def test_hash(self):
        assert hash(PCIDevice(0x1234, 0x5678, 0x9a)) == 0x123456789a

    def test_str(self):
        assert str(PCIDevice(0x1234, 0x5678, 0x9a)) == "0x1234:0x5678:0x9a"

    def test_from_str(self):
        assert PCIDevice.from_str("1234:5678:9a") == PCIDevice(0x1234, 0x5678, 0x9a)
        assert PCIDevice.from_str("0x1234:0x5678:0x9a") == PCIDevice(0x1234, 0x5678, 0x9a)

        assert PCIDevice.from_str("0x1234:5678") == PCIDevice(0x1234, 0x5678, 0x0)

        with self.assertRaises(ValueError):
            assert PCIDevice.from_str("0x1234:5678:0x12:045") == PCIDevice(0x1234, 0x5678, 0x0)
