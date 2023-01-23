"""
Module for IPv4 and IPv6 address handling
"""

import ipaddress


class IPv4NetworkHandling:
    """
    Wrapper class of ipaddress.IPv4Network for handling IPv4 Network addresses
    """
    def __init__(self, address):
        self.ipaddress_original = address

        # check for the case if host bits are set or not and create the network object accordingly
        try:
            self.ipv4network_object = ipaddress.IPv4Network(self.ipaddress_original)

        except ValueError:
            self.ipv4network_object = ipaddress.IPv4Network(self.ipaddress_original, strict=False)

    def get_object(self):
        """
        for returning the ipv4 network object
        :return: ipv4 network object
        """
        return self.ipv4network_object

    def version(self):
        """
        for returning the version of ipaddresses - ipv4/ipv6
        :return: the version of ipaddress - 4 should be returned in this case
        """
        return self.ipv4network_object.version

    def max_prefixlen(self):
        """
        for returning the maximum number of set bits in the net mask
        :return: maximum number of set bits in net mask
        """
        return self.ipv4network_object.max_prefixlen

    def network_address(self):
        """
        returns the network address of the ipaddress given
        :return: network address
        """
        return self.ipv4network_object.network_address.exploded

    def original_ipaddress(self):
        """
        returns the original ipaddress passed to the class
        :return: the original ipaddress
        """
        return self.ipaddress_original

    def hostmask(self):
        """
        returns the hostmask for the network
        :return: host mask for the network
        """
        return self.ipv4network_object.hostmask.exploded

    def netmask(self):
        """
        returns the net mask for the network - should be the inverted version of hostmask
        :return: the net mask for the network
        """
        return self.ipv4network_object.netmask.exploded

    def print_all_ipaddress_included(self):
        """
        prints all the ipaddresses allowed in the network
        """
        if self.ipv4network_object.network_address == self.ipaddress_original:
            print("The ip addresses in the network are as follows: -")

        else:
            print("The given ip address belongs to the following set of ip addresses: -")

        for addr in self.ipv4network_object:
            print(addr)

    def write_to_file_ipaddresses_included(self, filename):
        """
        writes all the ipaddresses allowed in the network to a file
        :param filename: the name of file to which the ipaddresses need to be written
        """
        data = ''
        for addr in self.ipv4network_object:
            data += str(addr)
            data += '\n'
        with open(filename, 'w', encoding='utf-8') as file:
            file.writelines(data)

    def count_number_of_ipaddresses(self):
        """
        returns the number of ipaddresses allowed in the network
        :return: count of ipaddresses
        """
        count = 0
        for _ in self.ipv4network_object:
            count += 1
        return count


class IPv6NetworkHandling:
    """
    Wrapper class for ipaddress.IPv6Network for ipv6 network address handling
    """
    def __init__(self, address):
        self.ipaddress_original = address

        # check for case where host bits are set and create the network object accordingly
        try:
            self.ipv6network_object = ipaddress.IPv6Network(self.ipaddress_original)

        except ValueError:
            self.ipv6network_object = ipaddress.IPv6Network(self.ipaddress_original, strict=False)

    def get_object(self):
        """
        returns the network object created
        :return: network object
        """
        return self.ipv6network_object

    def version(self):
        """
        returns the version of the ipaddress - ipv4/ipv6
        :return: the version of address - should be 6 for this class
        """
        return self.ipv6network_object.version

    def max_prefixlen(self):
        """
        returns the maximum number of set bits allowed for the version
        :return: maximum number of set bits allowed - should be 128 for this class
        """
        return self.ipv6network_object.max_prefixlen

    def network_address(self):
        """
        returns the network address for the ipaddress given
        :return: the network address
        """
        return self.ipv6network_object.network_address.exploded

    def original_ipaddress(self):
        """
        returns the original ipaddress passed to the class
        :return: the original ipaddress
        """
        return self.ipaddress_original

    def hostmask(self):
        """
        returns the host mask for the network
        :return: the host mask
        """
        return self.ipv6network_object.hostmask.exploded

    def netmask(self):
        """
        returns the net mask for the network - should be the inverted version of the host mask
        :return: the net mask
        """
        return self.ipv6network_object.netmask.exploded

    def print_all_ipaddress_included(self):
        """
        prints all the ip addresses allowed in the network
        """
        if self.ipv6network_object.network_address == self.ipaddress_original:
            print("The ip addresses in the network are as follows: -")

        else:
            print("The given ip address belongs to the following set of ip addresses: -")

        for addr in self.ipv6network_object:
            print(addr)

    def write_to_file_ipaddresses_included(self, filename):
        """
        writes all the ipaddresses allowed in the network to a file
        :param filename: the name of the file to which the ip addresses needs to be written
        """
        data = ''
        for addr in self.ipv6network_object:
            data += str(addr)
            data += '\n'
        with open(filename, 'w', encoding='utf-8') as file:
            file.writelines(data)

    def count_number_of_ipaddresses(self):
        """
        returns the number of ipaddresses allowed in the network
        :return: the count of the ipaddresses
        """
        count = 0
        for _ in self.ipv6network_object:
            count += 1
        return count


if __name__ == "__main__":
    ipv4_object1 = IPv4NetworkHandling('192.168.0.0/24')
    print(ipv4_object1.version())
    print(ipv4_object1.max_prefixlen())
    print(ipv4_object1.network_address())
    print(ipv4_object1.original_ipaddress())
    print(ipv4_object1.netmask())
    print(ipv4_object1.hostmask())
    ipv4_object1.print_all_ipaddress_included()

    ipv4_object2 = IPv4NetworkHandling('123.45.67.89/27')
    print(ipv4_object2.version())
    print(ipv4_object2.max_prefixlen())
    print(ipv4_object2.network_address())
    print(ipv4_object2.original_ipaddress())
    print(ipv4_object2.netmask())
    print(ipv4_object2.hostmask())
    ipv4_object2.print_all_ipaddress_included()
