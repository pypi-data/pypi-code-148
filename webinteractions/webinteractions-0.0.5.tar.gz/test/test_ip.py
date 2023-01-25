"""Tests ip_functions module"""

import unittest
import ipaddress
from webinteractions import get_ipv4address_generator, get_ipv6address_generator

class IPTestMethods(unittest.TestCase):
    """Class tests the ip_functions module"""
    
    def test_ipv4_address(self):
        generator = get_ipv4address_generator("192.168.0.0/27")
        self.assertEqual(len(list(generator)), 32)

    def test_ipv4_address_single(self):
        generator = get_ipv4address_generator("192.168.0.0/32")
        self.assertEqual(len(list(generator)), 1)

    def test_ipv4_address_two(self):
        generator = get_ipv4address_generator("192.168.0.0/31")
        self.assertEqual(len(list(generator)), 2)

    def test_ipv4_address_invalid_netmask(self):
        with self.assertRaises(ipaddress.NetmaskValueError):
            generator = get_ipv4address_generator("192.168.0.0/33")
            print(len(list(generator)))

    def test_ipv4_address_invalid_address(self):
        with self.assertRaises(ipaddress.AddressValueError):
            generator = get_ipv4address_generator("256.0.0.0/32")
            print(len(list(generator)))

    def test_ipv6_address(self):
        generator = get_ipv6address_generator("2001:db8::/122")
        self.assertEqual(len(list(generator)), 64)

    def test_ipv6_address_single(self):
        generator = get_ipv6address_generator("2001:db8::/128")
        self.assertEqual(len(list(generator)), 1)

    def test_ipv6_address_two(self):
        generator = get_ipv6address_generator("2001:db8::/127")
        self.assertEqual(len(list(generator)), 2)

    def test_ipv6_address_invalid_netmask(self):
        with self.assertRaises(ipaddress.NetmaskValueError):
            generator = get_ipv6address_generator("2001:db8::/130")
            print(len(list(generator)))

    def test_ipv6_address_invalid_address(self):
        with self.assertRaises(ipaddress.AddressValueError):
            generator = get_ipv4address_generator("2000:db8::/128")
            print(len(list(generator)))


if __name__ == "__main__":
    unittest.main()
