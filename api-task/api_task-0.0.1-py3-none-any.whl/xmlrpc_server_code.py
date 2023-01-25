"""
This module is the xmlrpc server
"""
from xmlrpc.server import SimpleXMLRPCServer

def fib(n):
    """
    This is a fibonacci series function

    Args:
        n is a value of type int
    Return:
        the function returns the (n)th number of the Fibonacci Series
    """
    if n==1 or n==2:
        return 1
    else:
        return fib(n-1)+fib(n-2)

def xmlrpc_server():
    """
    This function act as the server for xmlrpc_server to execute Fibonacci Program from a remote client server
    """
    server = SimpleXMLRPCServer(("localhost", 8000))
    print("Listening on port 8000...")
    server.register_function(fib, "fib")
    server.serve_forever()

if __name__ == '__main__':
    xmlrpc_server()