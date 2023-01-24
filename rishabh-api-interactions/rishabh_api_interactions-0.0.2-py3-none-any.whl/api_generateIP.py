# This module is used to generate ip addresses of a given range

import ipaddress


def check(ip_value, network):
    """ Method to verify IP address network"""
    if network:
        grp = ipaddress.IPv4Network
    else:
        grp = ipaddress.IPv6Network
    try:
        ip_value = grp(ip_value)
    except (ipaddress.AddressValueError, ValueError,ipaddress.NetmaskValueError):
        return None

    return ip_value


def generate_ip(ip_value):
    """ Methods generate an itr for a range of ip address"""
    ip_value = check(ip_value,True)
    if ip_value is None:
        ip_value = check(ip_value,False)

    if ip_value is None:
        print("Incorrect Network IP entered")
        return None

    data = []
    for ipaddr in ip_value:
        data.append(ipaddr)

    return data


if __name__ == '__main__':
    for ip_address in generate_ip('192.168.0.0/24'):
        print(ip_address)