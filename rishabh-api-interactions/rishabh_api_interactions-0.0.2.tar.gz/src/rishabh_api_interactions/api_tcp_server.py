# Module for implement TCP server

import socketserver


class server_handler(socketserver.BaseRequestHandler):
    """ The request handler class for the server """

    def handle(self):
        print("Enter anything")
        self._data = self.request.recv(1024).decode("utf-8")
        print("{} wrote: ".format(self.client_address[0]))
        print(self._data)
        self.request.sendall(bytes(self._data, 'utf-8'))


def main(host='localhost',port=9999):
    with socketserver.TCPServer((host, port), server_handler) as server:
        server.handle_request()


if __name__ == "__main__":
    main()
