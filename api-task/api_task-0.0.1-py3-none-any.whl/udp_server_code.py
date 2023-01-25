"""
This module is the UDP Server
"""
import socketserver

HOST = 'localhost'
PORT = 8088

class MyUDPHandler(socketserver.BaseRequestHandler):
    """
    This class works similar to the TCP handler class, except that
    self.request consists of a pair of data and client socket, and since
    there is no connection the client address must be given explicitly
    when sending data back via sendto().
    """

    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        print("{} wrote:".format(self.client_address[0]))
        print(data)
        socket.sendto(data.upper(), self.client_address)

def server_UDP():
    """
    This function starts the UDP Server and it should be started from a different terminal for tests to run successfully
    """
    with socketserver.UDPServer((HOST,PORT),MyUDPHandler) as server:
        server.serve_forever()

if __name__ == '__main__':
    server_UDP()