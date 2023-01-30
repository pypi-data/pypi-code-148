import unittest
from flex_algo import stack


class MyTestCase(unittest.TestCase):
    def test_is_valid(self):
        stk = stack.Stack()
        valid = stk.is_valid('()')
        self.assertEqual(valid, True)  # add assertion here

    def test_is_not_valid(self):
        stk = stack.Stack()
        valid = stk.is_valid("(]")
        self.assertEqual(valid, False)

    def test_min_remove_to_make_valid(self):
        stk = stack.Stack()
        valid_s = stk.min_remove_to_make_valid("a)b(c)d")
        self.assertEqual(valid_s, "ab(c)d")


if __name__ == '__main__':
    unittest.main()
