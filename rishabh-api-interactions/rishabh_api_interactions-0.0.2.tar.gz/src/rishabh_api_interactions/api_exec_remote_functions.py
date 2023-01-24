# This module is used to remotely execute server functions

import xmlrpc.client


def remote_function(server_url, a, b=2):
    server_proxy = xmlrpc.client.ServerProxy(server_url)
    try:
        return server_proxy.raise_power(a,b)
    except xmlrpc.client.Fault as err:
        print("A fault occurred")
        print("Fault code: %d" % err.faultCode)
        print("Fault string: %s" % err.faultString)
        return None


if __name__ == '__main__':
    print(remote_function("http://localhost:8000/", 5, 3))