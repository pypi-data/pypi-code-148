import unittest
from flex_algo import linked_list


class MyTestCase(unittest.TestCase):
    def test_reverse_between(self):
        llist = linked_list.LinkedList()
        llist.push_back(5)
        llist.reverse_between(1, 1)
        print(llist)

    def test_is_cyclic(self):
        llist = linked_list.LinkedList()
        llist.push_back(1)
        llist.push_back(2)
        llist.push_back(3)
        llist.push_back(4)
        llist.push_back(5)
        cyclic = llist.is_cyclic()
        self.assertEqual(cyclic, None)


if __name__ == '__main__':
    unittest.main()
