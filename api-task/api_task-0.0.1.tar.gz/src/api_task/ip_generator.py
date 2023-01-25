"""
This module is genereating ip addresses for a given CIDR network
"""
import ipaddress
import sys

def generate_ip(inp_ip):
    """
    This function will take input of the CIDR network and return list of range of IP addresses

    Args:
        It takes input of CIDR network of the form String
    
    Return:
        It returns a tuple which consists of the type of network and a list of IP addresses
    """
    addr = ipaddress.ip_network(inp_ip,strict=False)
    network_type = ""
    if addr.version == 4:
        network_type = "IPv4 Network"
    else:
        network_type = "IPv6 network"
    ip_list = []
    for individual_ip in addr.hosts():
        ip_list.append(individual_ip)
    return network_type,ip_list

if __name__ == '__main__':
    generate_ip(sys.argv[1])

