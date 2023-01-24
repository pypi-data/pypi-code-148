import socket
import sys


def main(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, port))
        sock.listen(1)
        conn, addr = sock.accept()
        with conn:
            print('Connected by', addr)
            conn.sendall(b"Enter username")
            username = conn.recv(1024)
            conn.sendall(b"Enter password")
            password = conn.recv(1024)
            if username == b"Rishabh" and password == b"Pallod":
                conn.sendall(b"Login successful")
            else:
                conn.sendall(b'Incorrect user details')
    return


if __name__ == "__main__":
    main('localhost', 50007)
