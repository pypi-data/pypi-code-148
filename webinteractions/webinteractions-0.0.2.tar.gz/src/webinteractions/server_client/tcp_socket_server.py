"""Provides functions that can start a tcp server either synchronous
    or threaded with a simple function call"""

import sys
import threading
import socketserver
from .utils import get_synchronous_response, get_threaded_response

class TCPRequestHandler(socketserver.BaseRequestHandler):
    """Defines how the request will be handled for a tcp synchronous server"""
    def handle(self):
        self.data = str(self.request.recv(1024).strip(), 'ascii')
        
        response = get_synchronous_response(self.data, self.client_address[0])

        self.request.sendall(response)


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    """Defines how the request will be handled for a tcp threaded server"""
    def handle(self):
        self.data = str(self.request.recv(1024), 'ascii')
        cur_thread = threading.current_thread()

        response = get_threaded_response(self.data, cur_thread.name, self.client_address[0])

        self.request.sendall(response)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """Class instance will create a tcp server running with threads"""
    pass


def create_tcp_synchronous(hostname="localhost", port=8000):
    """Function starts a tcp synchronous server listening on the
        given hostname and port number

        ARGS:
            hostname: hostname the tcp server is listening on
            port: port number the tcp server is listening on
    """

    with socketserver.TCPServer((hostname, port), TCPRequestHandler) as server:
        print("Listening on {}:{}".format(hostname, port))

        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received, exiting...")
            sys.exit(0)


def create_tcp_threaded(hostname="localhost", port=8000):
    """Function starts a tcp threaded server listening on the
        given hostname and port number

        ARGS:
            hostname: hostname the tcp server is listening on
            port: port number the tcp server is listening on
    """

    with ThreadedTCPServer((hostname, port), ThreadedTCPRequestHandler) as server:
        print("Listening on {}:{}".format(hostname, port))

        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received, exiting...")
            sys.exit(0)
