# This module is used to remotely execute server functions

import xmlrpc.client


class ExecRemote:
    """ Class to remotely run floor divide function on a server """
    def __init__(self):
        self._server_proxy = None

    def remote_function(self, server_url, a, b=2):
        """ Method to remotely access raise power function on the server
            :arg: server_url : Takes the host and port details of server
            :arg: a, b : int objs as input for floor_divide method

            :returns: int obj on success and None on failure
        """
        self._server_proxy = xmlrpc.client.ServerProxy(server_url)
        try:
            return self._server_proxy.floor_divide(a, b)
        except xmlrpc.client.Fault as err:
            print("A fault occurred")
            print("Fault code: %d" % err.faultCode)
            print("Fault string: %s" % err.faultString)
            return None


if __name__ == '__main__':
    print(ExecRemote().remote_function("http://localhost:8000/", 5, 3))
