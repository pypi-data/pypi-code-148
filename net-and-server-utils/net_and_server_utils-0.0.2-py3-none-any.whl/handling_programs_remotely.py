"""
Module for handling programs running on remote server
"""
from xmlrpc import client, server


class XMLRPCClientInterface:
    """
    Wrapper class for xmlrpc module and xmlrpc client in standard library
    """
    def __init__(self):
        self.host = None
        self.port = None
        self.proxy = None

    def create_client_proxy(self, host, port):
        """
        for creating a client proxy for the xmlrpc server
        :param host: host address
        :param port: port number
        """
        self.host = host
        self.port = port
        self.proxy = client.ServerProxy(f'http://{self.host}:{self.port}')

    def get_methods_server_program(self):
        """
        helper function for methods supported by xmlrpc server
        :return:list of methods/functions
        """
        try:
            return self.proxy.system.listMethods()
        except AttributeError:
            print("The server doesn't allow to look into its methods")
            return None

    def remote_server_response(self, function_name, arguments):
        """
        for response of specific function supported by the server
        :param function_name: the name of the function - string
        :param arguments: arguments required by the functions in a form of a list
        :return: the result of the function call or Fault Error or Protocol Error
        """
        try:
            with self.proxy as proxy:
                func = getattr(proxy, function_name)
                return func(arguments)

        except client.Fault as error:
            print("Fault Error")
            print(f'Fault Code: {error.faultCode}')
            print(f"Fault Description: {error.faultString}")
            return None

        except client.ProtocolError as error:
            print("Protocol Error")
            print(f"Error URL: {error.url}")
            print(f"Headers: {error.headers}")
            print(f"Error Code: {error.errcode}")
            print(f"Error Description: {error.errmsg}")
            return None


class XMLRPCServerCreation:
    """
    Wrapper class for xmlrpc module and xmlrpc server
    """
    def __init__(self):
        self.host = None
        self.port = None
        self.server = None

    def create_server(self, host, port):
        """
        for initiating the server
        :param host: the host address - string
        :param port: the port number - integer
        """
        self.server = server.SimpleXMLRPCServer((host, port))
        self.server.register_introspection_functions()

    def register_functions(self, functions_list):
        """
        for registering the functions to the server
        :param functions_list: list of functions
        """
        for function in functions_list:
            self.server.register_function(function, function.__name__)

    def start_server_forever(self):
        """
        for starting the server for forever
        """
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            print('closing server...')
            self.server.close()
