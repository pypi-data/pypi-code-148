# Module for implement TCP server

import socketserver


class server_handler(socketserver.BaseRequestHandler):
    """ The request handler class for the server """

    def handle(self):
        """Method to echo user response"""
        print("Enter anything")
        self._data = self.request.recv(1024).decode("utf-8")
        print("{} wrote: ".format(self.client_address[0]))
        print(self._data)
        self.request.sendall(bytes(self._data, 'utf-8'))


def creating_tcp_server(host='localhost',port=9999):
    """ Method to activate tcp server
    :param: host: Host to connect
    :param: port: port to connect
    """
    with socketserver.TCPServer((host, port), server_handler) as server:
        server.handle_request()


if __name__ == "__main__":
    creating_tcp_server()
