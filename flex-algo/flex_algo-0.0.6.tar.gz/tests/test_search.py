import unittest
from flex_algo import search


class MyTestCase(unittest.TestCase):
    def test_binary_search(self):
        arr = [1, 2, 3, 4, 5, 6, 7, 8]
        idx = search.binary_search(arr, 5)
        self.assertEqual(idx, 4)  # add assertion here


if __name__ == '__main__':
    unittest.main()
