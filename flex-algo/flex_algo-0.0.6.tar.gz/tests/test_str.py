import unittest
from flex_algo import array_utils

class MyTestCase(unittest.TestCase):
    def test_backspace_compare(self):
        s, t = "ab#c", "ad#c"
        same = str_utils.backspace_compare(s, t)
        self.assertEqual(same, True)  # add assertion here

if __name__ == '__main__':
    unittest.main()
