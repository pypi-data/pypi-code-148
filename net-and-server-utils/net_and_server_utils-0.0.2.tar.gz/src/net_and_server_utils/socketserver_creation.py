"""
Module for socket server creation - TCP/UDP as well as clients for the same
"""
import socketserver
import socket


class TCPHandler(socketserver.StreamRequestHandler):
    """
    Request handler class for the TCP server
    """
    def handle(self):
        """
        for handling the requests, overrides the handle method of the base class
        """
        data = self.rfile.readline().strip()
        print(f'{self.client_address[0]} wrote: ')
        print(data)
        self.wfile.write(data)


class UDPHandler(socketserver.BaseRequestHandler):
    """
    Request handling class for UDP Server
    """
    def handle(self):
        """
        for handling requests to the server, overrides the handle method of the base class
        """
        data = self.request[0].strip()
        sock = self.request[1]
        print(f'{self.client_address[0]} wrote: ')
        print(data)
        sock.sendto(data, self.client_address)


class TCPServerCreation:
    """
    Wrapper class of socketserver.TCPServer for TCP Server creation
    """
    def __init__(self):
        self.tcp_server = None
        self.port = None

    def create_server(self, host, port):
        """
        initiates the server
        :param host: the host address - str
        :param port: the port number - int
        """
        self.port = port
        try:
            self.tcp_server = socketserver.TCPServer((host, port), TCPHandler)
            print('TCP server successfully created\n')
        except PermissionError:
            print("Unable to bind server to the port. Try a different port number.")
        except OSError:
            print("This server with the port number is already running")

    def get_server_address(self):
        """
        returns the server address for the server created
        :return: the server address - str
        """
        return self.tcp_server.server_address[0]

    def get_port(self):
        """
        returns the port number of the server
        :return: the port number - int
        """
        return self.port

    def start_server(self):
        """
        starts the server for handling single request only
        shuts down after the request has been handled
        """
        with self.tcp_server as current_server:
            try:
                print('server started\n')
                current_server.handle_request()
            except KeyboardInterrupt:
                print('closing server')
                current_server.server_close()
                current_server.shutdown()

    def start_server_for_forever(self, poll_interval=0.5):
        """
        starts the server for handling infinite requests
        shuts down only after a keyboard interrupt is performed
        :param poll_interval: the time interval after which the shut-down request will be polled
        """
        with self.tcp_server as current_server:
            try:
                print('server started\n')
                current_server.serve_forever(poll_interval=poll_interval)
            except KeyboardInterrupt:
                print('closing server')
                current_server.server_close()


class TCPSocketClient:
    """
    For creating a client for communicating to a server over TCP protocol
    """
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def communicate(self):
        """
        starts the communication with the server over TCP protocol
        """
        while True:
            client_input = input('Enter the data to be communicated: ')
            if client_input == 'disconnect':
                break
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                # Connect to server and send data

                sock.connect((self.host, self.port))
                sock.sendall(bytes(client_input + "\n", "utf-8"))

                # Receive data from the server and shut down
                received = str(sock.recv(1024), "utf-8")

            print(f"Sent :    {client_input}")
            print(f"Received: {received}")

    def communicate_and_save(self, filename):
        """
        starts communicating with the server over TCP Protocol
        writes the results received to a file
        :param filename: the name of the file to which the results are to be written
        """
        while True:
            client_input = input('Enter the data to be communicated: ')
            if client_input == 'disconnect':
                break
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                # Connect to server and send data

                sock.connect((self.host, self.port))
                sock.sendall(bytes(client_input + "\n", "utf-8"))

                # Receive data from the server and shut down
                received = str(sock.recv(1024), "utf-8")

            print(f"Sent:     {client_input}")
            print(f"Received: {received}")
            with open(filename, 'a', encoding='utf-8') as file:
                file.write(received + '\n')


class UDPServerCreation:
    """
    Wrapper class for socketserver.UDPServer for UDP server creation
    """
    def __init__(self):
        self.udp_server = None
        self.port = None

    def create_server(self, host, port):
        """
        initiates the server using UDP protocol
        :param host: the host address - str
        :param port: the port number - int
        """
        self.port = port
        try:
            self.udp_server = socketserver.UDPServer((host, port), UDPHandler)
            print('UDP server successfully created\n')
        except PermissionError:
            print("Unable to bind server to the port. Try a different port number.")
        except OSError:
            print("This server with the port number is already running")

    def get_server_address(self):
        """
        returns the UDP server address
        :return: the server address - str
        """
        return self.udp_server.server_address[0]

    def get_port(self):
        """
        returns the port number of the server
        :return: the port number - int
        """
        return self.port

    def start_server(self):
        """
        starts the server for handling one single request
        shuts down once the request has been handled
        """
        with self.udp_server as current_server:
            try:
                print('server started\n')
                current_server.handle_request()
            except KeyboardInterrupt:
                print('closing server')
                current_server.server_close()
                current_server.shutdown()

    def start_server_for_forever(self, poll_interval=0.5):
        """
        starts the server for infinite requests
        shuts down only when a keyboard interrupt is performed
        :param poll_interval: the interval in secs after which the shutdown poll is performed
        """
        with self.udp_server as current_server:
            try:
                print('server started\n')
                current_server.serve_forever(poll_interval=poll_interval)
            except KeyboardInterrupt:
                print('closing server')
                current_server.server_close()


class UDPSocketClient:
    """
    for creating a client to communicate with a server over UDP protocol
    """
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def communicate(self):
        """
        starts communication with the server over UDP protocol
        """
        while True:
            client_input = input('Enter the data to be communicated: ')
            if client_input == 'disconnect':
                break
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # Connect to server and send data

            sock.sendto(bytes(client_input + "\n", "utf-8"), (self.host, self.port))

            # Receive data from the server and shut down
            received = str(sock.recv(1024), "utf-8")

            print(f"Sent:     {client_input}")
            print(f"Received: {received}")

    def communicate_and_save(self, filename):
        """
        starts communication with the server over UDP protocol
        writes the response received from the server to file
        :param filename: the name of the file
        """
        while True:
            client_input = input('Enter the data to be communicated: ')
            if client_input == 'disconnect':
                break
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # Connect to server and send data

            sock.sendto(bytes(client_input + "\n", "utf-8"), (self.host, self.port))

            # Receive data from the server and shut down
            received = str(sock.recv(1024), "utf-8")

            print(f"Sent:     {client_input}")
            print(f"Received: {received}")
            with open(filename, 'a', encoding='utf-8') as file:
                file.write(received + '\n')


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080
    server = TCPServerCreation()
    server.create_server(HOST, PORT)
    server.start_server_for_forever()

    udp_server = UDPServerCreation()
    udp_server.create_server(HOST, PORT)
    udp_server.start_server_for_forever()
