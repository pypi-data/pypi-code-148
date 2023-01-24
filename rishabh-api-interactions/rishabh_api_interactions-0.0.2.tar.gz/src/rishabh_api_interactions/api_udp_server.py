# Module for implement UDP server

import socketserver


class server_handler(socketserver.BaseRequestHandler):
    """ The request handler class for the server """

    def handle(self):
        self._data = self.request[0].strip()
        self._socket = self.request[1]
        print("{} wrote: ".format(self.client_address[0]))
        print(self._data.decode("utf-8"))
        self._socket.sendto(self._data, self.client_address)
        return


def main():
    host, port = "localhost", 9999

    with socketserver.UDPServer((host, port), server_handler) as server:
        server.handle_request()


if __name__ == "__main__":
    main()
