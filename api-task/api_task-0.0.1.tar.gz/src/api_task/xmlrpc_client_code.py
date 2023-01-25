"""
This module is the xmlrpc client
"""
import xmlrpc.client

def xmlrpc_client(data):
    """
    This function acts as the client for xmlrpc server

    Args:
        data is a list of elements each of type int who's fibonacci number are to be calculated
    
    Return:
        function returns a list of string with Fibonacci Number for each element in the Args
    """
    res = []
    with xmlrpc.client.ServerProxy("http://localhost:8000/") as proxy:
        for items in data:
            res.append("{} number in Fibonacci Series: {}".format(items,str(proxy.fib(items))))
        return res

if __name__ == '__main__':
    data = []
    xmlrpc_client(data)