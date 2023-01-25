"""Tests xmlrpc_wrapper module"""

import xmlrpc
import unittest
from webinteractions.server_client.xmlrpc_wrapper import get_server_proxy

class XmlrpcTestMethods(unittest.TestCase):
    """Class contains test cases for xmlrpc_wrapper"""
    def setUp(self):
        """Server must be started separately"""
        self.proxy = get_server_proxy()
    
    def test_add(self):
        self.assertEqual(self.proxy.add(5, 3), 8)

    def test_add_2(self):
        self.assertEqual(self.proxy.add("test", "2"), "test2")

    def test_multiply(self):
        self.assertEqual(self.proxy.mult(5, 3), 15)

    def test_multiply_array(self):
        self.assertEqual(self.proxy.mult([0], 3), [0, 0, 0])

    def test_pow(self):
        self.assertEqual(self.proxy.pow(2, 5), 32)

    def test_pow_2(self):
        self.assertEqual(self.proxy.pow(2, 10), 1024)

    def test_unhandled(self):
        with self.assertRaises(xmlrpc.client.Fault):
            self.proxy.test(2)


if __name__ == "__main__":
    unittest.main()
