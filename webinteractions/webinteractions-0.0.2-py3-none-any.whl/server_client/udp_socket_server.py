"""Provides functions that can start a udp server either synchronous
    or threaded with a simple function call"""

import sys
import threading
import socketserver
from .utils import get_synchronous_response, get_threaded_response

class UDPRequestHandler(socketserver.BaseRequestHandler):
    """Defines how the request will be handled for a udp synchronous server"""
    def handle(self):
        self.data = str(self.request[0].strip(), 'ascii')

        response = get_synchronous_response(self.data, self.client_address[0])

        self.request[1].sendto(response, self.client_address)


class ThreadedUDPRequestHandler(socketserver.BaseRequestHandler):
    """Defines how the request will be handled for a udp synchronous server"""
    def handle(self):
        self.data = str(self.request[0].strip(), 'ascii')
        cur_thread = threading.current_thread()

        response = get_threaded_response(self.data, cur_thread.name, self.client_address[0])

        self.request[1].sendto(response, self.client_address)


class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    """Class instance will create a udp server running with threads"""
    pass


def create_udp_synchronous(hostname="localhost", port=8000):
    """Function starts a udp synchronous server listening on the
        given hostname and port number

        ARGS:
            hostname: hostname the udp server is listening on
            port: port number the udp server is listening on
    """
    with socketserver.UDPServer((hostname, port), UDPRequestHandler) as server:
        print("Listening on {}:{}".format(hostname, port))

        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received, exiting...")
            sys.exit(0)


def create_udp_threaded(hostname="localhost", port=8000):
    """Function starts a udp threaded server listening on the
        given hostname and port number

        ARGS:
            hostname: hostname the udp server is listening on
            port: port number the udp server is listening on
    """
    with ThreadedUDPServer((hostname, port), ThreadedUDPRequestHandler) as server:
        print("Listening on {}:{}".format(hostname, port))

        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("\nKeyboard interrupt received, exiting...")
            sys.exit(0)
