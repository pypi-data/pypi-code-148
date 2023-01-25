"""
This module is the client for the UDP Server
"""
import socket
import sys


HOST, PORT = "localhost", 8088
data = " ".join(sys.argv[1:])

def start_server_UDP(data):
    """
    This function acts as the client for UDP Server

    Args:
        data is value of type string which is to be executed on the server
    
    Return:
        This function recieves the data and returns the recieved data
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.sendto(bytes(data + "\n", "utf-8"), (HOST, PORT))
    received = str(sock.recv(1024), "utf-8")
    
    # print("Sent:     {}".format(data))
    # print("Received: {}".format(received))
    return received

if __name__ == '__main__':
    start_server_UDP(data)
