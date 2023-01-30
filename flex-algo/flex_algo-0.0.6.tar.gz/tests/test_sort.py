import unittest
from flex_algo import sort


class MyTestCase(unittest.TestCase):
    def test_quick_sort(self):
        arr = [3, 2, 1, 5, 6, 4]
        sort.quick_sort(arr)
        self.assertEqual(arr, [1, 2, 3, 4, 5, 6])  # add assertion here

    def test_quick_select(self):
        arr = [3, 2, 1, 5, 6, 4]
        kth = sort.quick_select(arr, 2)
        self.assertEqual(kth, 5)

        arr2 = [3, 2, 3, 1, 2, 4, 5, 5, 6]
        kth2 = sort.quick_select(arr2, 4)
        self.assertEqual(kth2, 4)


if __name__ == '__main__':
    unittest.main()
