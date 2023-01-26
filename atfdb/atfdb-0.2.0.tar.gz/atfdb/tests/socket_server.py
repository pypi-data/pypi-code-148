"""
Based on https://www.digitalocean.com/community/tutorials/python-socket-programming-server-client.
"""
import datetime
import os
import socket

from numpy.random import default_rng


def print_log(msg):
    print(f"{datetime.datetime.now().isoformat()} {msg}")


def server_program(seed=0):
    # get the hostname
    host = os.getenv("ATF_SOCKET_HOST", "localhost")
    port = int(os.getenv("ATF_SOCKET_PORT", 5000))  # initiate port no above 1024

    recv_buffer_size = int(os.getenv("ATF_DB_RECEIVE_BUFFER_SIZE", 5120))
    send_buffer_size = int(os.getenv("ATF_DB_SEND_BUFFER_SIZE", 5120))  # noqa F841

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print_log("Connection from: " + str(address))
    data = "greeting"
    conn.send(data.encode())  # send data to the client

    rng = default_rng(seed)

    while True:
        # receive data stream. it won't accept data packet greater than `recv_buffer_size` bytes
        data = conn.recv(recv_buffer_size).decode()
        if not data:
            # if data is not received break
            break
        data = str(data)
        print_log(f"from connected user: {data}")
        if data.startswith("GETCHIDX"):
            reply = f"{rng.integers(0, 100)}"
            print_log(f"reply to client: {reply}")
            conn.send(reply.encode())  # send data to the client
        elif data.startswith(("GETRS", "GETDS")):
            reply = f"{rng.random()}"
            print_log(f"reply to client: {reply}")
            conn.send(reply.encode())  # send data to the client
        elif data.startswith(("PUTRS", "PUTDS")):
            reply = f"PUTOK {data.split()[-1]}"
            print_log(f"reply to client: {reply}")
            conn.send(reply.encode())  # send data to the client
        else:
            print_log(f"{data = }")
    conn.close()  # close the connection


if __name__ == "__main__":
    server_program()
