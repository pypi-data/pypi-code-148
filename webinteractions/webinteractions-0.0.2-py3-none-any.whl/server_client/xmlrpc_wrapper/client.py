"""Module containing client side functions for xmlrpc"""

from xmlrpc import client

def get_server_proxy(hostname="localhost", port=8000, protocol="http"):
    """Function will return a server proxy for the running xmlrpc server
        The proxy can be used to invoke functions registered on the server

        ARGS:
            hostname: hostname of the hosted server
            port: port of the hosted server
            protocol: supported protocol by the hosted server eg. http/https
    """

    server_proxy = client.ServerProxy("{}://{}:{}".format(protocol, hostname, port))

    print("Set the server proxy to {}://{}:{}".format(protocol, hostname, port))

    return server_proxy


if __name__ == "__main__":
    s = get_server_proxy()

    print(s.add(6, 8))
    print(s.echo("TEST"))
