"""
API to implement a network service involving sockets where
servers and clients authenticate themselves and encrypt the
transmitted data using SSL
"""

import ssl
import socket


class SSLSocketClient:
    """
    Class for creating client using SSL sockets
    """
    def __init__(self):
        self.context = None
        self.server_hostname = None
        self.port = None
        self.client_instance = None
        self.server_cert = None

    def default_context_creation(self):
        """
        creates the context with default configuration
        """
        self.context = ssl.create_default_context()

    def manual_context_creation(self, certificates_location):
        """
        for manual creation of context
        :param certificates_location: the location where the certificates are stored
        """
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        self.context.load_verify_locations(certificates_location)

    def connect_to_server(self, server_hostname, port_number):
        """
        connects to the desired server
        :param server_hostname: host name of the server
        :param port_number: port number on which server is listening
        :raises SSLCertVerificationError - when the SSL certificate cannot be verified
        """
        self.server_hostname = server_hostname
        self.port = port_number
        self.client_instance = self.context.wrap_socket(socket.socket(socket.AF_INET),
                                                        server_hostname=self.server_hostname)
        self.client_instance.connect((self.server_hostname, self.port))

    def get_server_certificate(self):
        """
        retrieve the server certificate
        :return: server's SSL certificate
        """
        self.server_cert = self.client_instance.getpeercert()
        return self.server_cert

    def communicate(self):
        """
        for communicating with the server and printing the response
        """
        while True:
            client_input = input("Enter the data to be transmitted: ")
            if client_input == 'disconnect':
                print("disconnecting from the server...")
                print(" ")
                break
            self.client_instance.sendall(bytes(client_input + '\n', 'utf-8'))
            received_data = str(self.client_instance.recv(1024), 'utf-8')
            print(f"Received data: {received_data}")

    def communicate_and_save(self, filename):
        """
        communicates with the server and saves the response to a file
        :param filename: the name of file where the response needs to be stored
        """
        while True:
            client_input = input("Enter the data to be transmitted: ")
            if client_input == 'disconnect':
                print("disconnecting from the server....")
                print(" ")
                break
            self.client_instance.sendall(bytes(client_input, 'utf-8'))
            received_data = str(self.client_instance.recv(1024), 'utf-8')
            print(f"Received data: {received_data}")
            with open(filename, 'a', encoding='utf-8') as file:
                file.write(received_data + '\n')


class SSLSocketServer:
    """
    Class for creating server using SSL Sockets
    """
    def __init__(self):
        self.certificate_file = None
        self.private_key_file = None
        self.hostname = None
        self.port = None
        self.context = None
        self.server_socket = None

    def create_context(self, certificate_file, private_key_file):
        """
        creates context with default configuration
        :param certificate_file: location of server's certificate file
        :param private_key_file: location of server's private key file
        """
        self.certificate_file = certificate_file
        self.private_key_file = private_key_file
        self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.context.load_cert_chain(self.certificate_file, self.private_key_file)

    def bind_and_listen(self, hostname, port):
        """
        binds the server with the host name and starts listening to requests
        :param hostname: host name/address of the server
        :param port: port number on which server needs to be run
        """
        self.hostname = hostname
        self.port = port
        self.server_socket = socket.socket()
        self.server_socket.bind((self.hostname, self.port))
        self.server_socket.listen(5)

    def accept_and_process_requests(self):
        """
        accepts the requests from the client and processes it
        """
        while True:
            new_socket, from_addr = self.server_socket.accept()
            conn_stream = self.context.wrap_socket(new_socket, server_side=True)
            try:
                data = str(conn_stream.recv(1024), 'utf-8')
                print(f'Received data: {data}')
            finally:
                conn_stream.shutdown(socket.SHUT_RDWR)
                conn_stream.close()
