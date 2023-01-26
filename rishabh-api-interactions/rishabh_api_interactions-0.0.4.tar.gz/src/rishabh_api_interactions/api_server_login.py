import socket


class ServerLogin:
    """ Class to create a server login protocol """
    def __init__(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._conn, self._addr = None, None
        self._username, self._password = None, None

    def creating_server(self, host, port):
        """ Method to activate server and login into it
        :param host: host to connect
        :param port: port number to connect
        """
        with self._sock:
            self._sock.bind((host, port))
            self._sock.listen(1)
            self._conn, self._addr = self._sock.accept()
            with self._conn:
                print('Connected by', self._addr)
                self._conn.sendall(b"Enter username")
                self._username = self._conn.recv(1024)
                self._conn.sendall(b"Enter password")
                self._password = self._conn.recv(1024)
                if self._username == b"Rishabh" and self._password == b"Pallod":
                    self._conn.sendall(b"Login successful")
                else:
                    self._conn.sendall(b'Incorrect user details')
        return


if __name__ == "__main__":
    ServerLogin().creating_server('localhost', 50007)
