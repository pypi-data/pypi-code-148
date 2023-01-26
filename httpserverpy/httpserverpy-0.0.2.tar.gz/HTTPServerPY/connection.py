"""Manage socket connection."""

import socket

def init(host, port) -> tuple:
    """Initialise the socket connection

    :param host: str - the server host
    :param host: str - the server port
    :return tuple socket connection and host + port
    """
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 100)
    connection.bind((host, port))
    connection.listen(10)
    print(f'Server started at {host}:{port}')
    return (connection, (host, port))


def close(connection: socket) -> None:
    """Close the socket connection

    :param connection: socket - Connection to close
    """
    connection.close()
