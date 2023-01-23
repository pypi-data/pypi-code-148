"""Functions will return a genetor for ipv4 and ipv6 address
    given a CIDR address"""

from ipaddress import IPv4Network, IPv6Network, AddressValueError, NetmaskValueError

def get_ipv4address_generator(network):
    """Function returns a generator that returns IPv4 addresses
        depending on the CIDR network provided

        ARGS:
            network: string containing CIDR network. Network format can be
            ip address and optional mask, integer that fits into 32 bits, integer byte
            object of length 4, big-endian or a two tuple of an address description
            and a netmask
    """
    try:
        addresses = IPv4Network(network, strict=False)
    except AddressValueError:
        print("{} is an Invalid IPv4 network".format(network))
        raise
    except NetmaskValueError:
        print("Invalid Netmask provided for IPv4 network")
        raise

    for addr in addresses:
        yield addr


def get_ipv6address_generator(network):
    """Function returns a generator that returns IPv6 addresses
        depending on the CIDR network provided

        ARGS:
            network: string containing CIDR network. Network format can be
            ip address and optional mask, integer that fits into 128 bits, integer byte
            object of length 16, big-endian or a two tuple of an address description
            and a netmask
    """
    try:
        addresses = IPv6Network(network, strict=False)
    except AddressValueError:
        print("{} is an Invalid IPv6 network".format(network))
        raise
    except NetmaskValueError:
        print("Invalid Netmask value provided for IPv6 network")
        raise

    for addr in addresses:
        yield addr
