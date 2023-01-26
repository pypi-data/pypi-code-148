from .logger import logger

import socket


class SerialConsoleTCPServer:
    def __init__(self, machine_id):
        self.id = machine_id

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('', 0))
        self.server.listen(1)

        self.client = None

        self.server_for_logs = LogClientTCPServer()

    @property
    def port(self):
        return self.server.getsockname()[1]

    @property
    def fileno_client(self):
        if self.client is None:
            return None

        return self.client.fileno()

    @property
    def fileno_server(self):
        return self.server.fileno()

    @property
    def fileno_servers(self):
        return [self.fileno_server, self.server_for_logs.fileno_server]

    def accept(self, fd):
        if fd == self.server_for_logs.fileno_server:
            return self.server_for_logs.accept()
        else:
            client, _ = self.server.accept()

            if self.client is not None:
                client.send(b"A client is already connected, re-try later!\r\n")
                client.shutdown(socket.SHUT_RDWR)
                client.close()
            else:
                self.client = client

    def send(self, buf):
        client = self.client
        if client is None:
            return

        try:
            client.send(buf)
        except (ConnectionResetError, BrokenPipeError, OSError):
            self.close_client()
        finally:
            # Finally, handle all the log clients
            self.server_for_logs.send(buf)

    def recv(self, size=8192):
        client = self.client
        if client is not None:
            try:
                buf = self.client.recv(size)
                if len(buf) == 0:
                    self.close_client()
                return buf
            except (ConnectionResetError, BrokenPipeError, OSError):
                self.close_client()

        return b""

    def close_client(self):
        logger.info("Closing the connection for the client of %s", self.id)

        client = self.client

        self.client = None

        if client is not None:
            client.shutdown(socket.SHUT_RDWR)
            client.close()


class LogClientTCPServer:
    """
    This class provides a TCP server that will manage communication
    with multiple clients that are only able to write, but not to read.
    """

    def __init__(self):
        self.server_ro = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_ro.bind(('', 0))
        self.server_ro.listen(20)

        self.clients_list = []

    @property
    def port(self):
        return self.server_ro.getsockname()[1]

    @property
    def fileno_server(self):
        return self.server_ro.fileno()

    def accept(self):
        client, _ = self.server_ro.accept()

        if len(self.clients_list) >= 25:
            client.send(b"Reached the maximum number of log clients for this machine, re-try later!\r\n")
            self.close_client(client)
        else:
            # This client is write-only, closing the read side
            client.shutdown(socket.SHUT_RD)
            self.clients_list.append(client)

    def send(self, buf):
        if self.clients_list:
            for client in self.clients_list:
                try:
                    client.send(buf)
                # Catch all exceptions, it doesn't matter for log users
                except Exception:
                    self.close_client(client)

    def close_client(self, client):
        try:
            client.shutdown(socket.SHUT_RDWR)
            client.close()
        except Exception as e:
            logger.info(f"Failed to close a client socket: {e}")
        finally:
            try:
                self.client_list.remove(client)
            except Exception:
                # The client was not on the list, so nothing to do
                pass
