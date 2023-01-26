# This module is used to generate ip addresses of a given range

import ipaddress


class IpGeneration:
    """ Class for generation of range of ip addresses """

    def __init__(self, input_ip):
        self._input_ip = input_ip
        self._ip_value = None
        self._data = []

    def check(self, network):
        """ Method to verify IP address network
        :param: user entered ip address
        :param: bool obj for Ip version
        :returns: IP address value or none in case of failure
        """
        if network:
            grp = ipaddress.IPv4Network
        else:
            grp = ipaddress.IPv6Network
        try:
            self._ip_value = grp(self._input_ip)
        except (ipaddress.AddressValueError, ValueError, ipaddress.NetmaskValueError):
            return
        return

    def generate_ip(self):
        """ Methods generate an itr for a range of ip address
        :param: user input ipaddress
        :returns: Range of ip address and None in case of incorrect input
        """
        self.check(True)
        if self._ip_value is None:
            self.check(False)

        if self._ip_value is None:
            print("Incorrect Network IP entered")
            return None

        for ipaddr in self._ip_value:
            self._data.append(ipaddr)

        return self._data


if __name__ == '__main__':
    for ip_address in IpGeneration('192.168.0.0/24').generate_ip():
        print(ip_address)
