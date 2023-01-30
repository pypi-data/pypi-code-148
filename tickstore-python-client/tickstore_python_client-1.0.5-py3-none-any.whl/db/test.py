import unittest
from .delta_buffer import DeltaBuffer
from ctypes import *


class TestStruct(Structure):
    _fields_ = [("x", c_uint64), ("y", c_uint64)]


class TestDeltaBuffer(unittest.TestCase):
    def test_append(self):
        """
        Test delta buffer
        """

        typ = TestStruct()
        delta_buffer = DeltaBuffer(TestStruct, None)

        # append multiple structs
        for i in range(100):
            typ.x = i
            typ.y = i+1
            delta_buffer.append(typ)

        i = 0
        for typ in delta_buffer:
            self.assertEqual(typ.x, i)
            self.assertEqual(typ.y, i+1)
            i += 1

    def test_get_set(self):
        """
        Test delta buffer
        """

        typ = TestStruct()
        delta_buffer = DeltaBuffer(TestStruct, None)

        # allocate 100
        for i in range(100):
            delta_buffer.append(typ)

        # set multiple structs
        for i in range(100):
            typ.x = i
            typ.y = i + 1
            delta_buffer[i] = typ

        for i in range(100):
            self.assertEqual(delta_buffer[i].x, i)
            self.assertEqual(delta_buffer[i].y, i + 1)


if __name__ == '__main__':
    unittest.main()