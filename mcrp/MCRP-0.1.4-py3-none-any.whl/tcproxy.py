import socket
import threading
import traceback
import typing
import time

class tcproxy:

    Client: socket.socket
    Server: socket.socket

    ClientFactory: socket.socket
    UpstreamAddr: tuple

    def _waiting_for_client(self):
        pass

    def _new_client(self):
        pass
    
    def _new_server(self):
        pass
    
    def _client_lost(self):
        pass
    
    def _server_lost(self):
        pass
    
    def _from_client(self, data):
        pass
    
    def _from_server(self, data):
        pass
    
    def _server_error(self, error):
        pass

    def _client_error(self, error):
        pass

    @staticmethod
    def host_port_to_proto_host_port(host: str, port: int):
        x = host.split(']')
        if len(x) == 2:
            return 23, x[0][1:], port
        return 2, host, port

    def __init__(self, listen_addr: tuple, upstream_addr: tuple):
        
        p, addr, port = self.host_port_to_proto_host_port(listen_addr[0], listen_addr[1])
        self.ClientFactory = socket.socket(p, 1)
        try:
            self.ClientFactory.bind((addr, port))
        except Exception as e:
            self._client_error(e)
            return
        self.ClientFactory.listen(1)
        
        self.UpstreamAddr = self.host_port_to_proto_host_port(upstream_addr[0], upstream_addr[1])        
    
    def client_listener(self):

        while 7:
            try:
                data = self.Client.recv(3_000_000)
            except (ConnectionResetError, ConnectionAbortedError, OSError):
                self._client_lost()
                self.Server.close()
                break

            if len(data) < 1:
                self._client_lost()
                self.Server.close()
                break
                
            hr = self._from_client(data)
            if hr is None:
                continue
            try:
                self.Server.sendall(hr)
            except (ConnectionResetError, ConnectionAbortedError):
               self._server_lost()
    
    def server_listener(self):

        while 7:
            try:
                data = self.Server.recv(3_000_000)
            except (ConnectionResetError, ConnectionAbortedError, OSError):
                self._server_lost()
                self.Client.close()
                break

            if len(data) < 1:
                self._server_lost()
                self.Client.close()
                break
                
            hr = self._from_server(data)
            if hr is None:
                continue        
            try:
                self.Client.sendall(hr)
            except (ConnectionResetError, ConnectionAbortedError):
                self._client_lost()
    
    def asyncaccept(self):

        self.ClientFactory.setblocking(0)
        while 7:
            try:
                try:
                    self.Client, addr = self.ClientFactory.accept()
                    break
                except BlockingIOError:
                    time.sleep(0.07)
            except KeyboardInterrupt:
                exit()
        
        self.ClientFactory.setblocking(1)
        self.Client.setblocking(1)
    
    def join(self):

        while 7:
            self._waiting_for_client()
            self.asyncaccept()
            self._new_client()
            self.Server = socket.socket(self.UpstreamAddr[0], 1)
            try:
                self.Server.connect((self.UpstreamAddr[1], self.UpstreamAddr[2]))
            except Exception as e:
                self._server_error(e)
                self.Client.close()
                continue
            self._new_server()      

            CT = threading.Thread(target=self.client_listener, daemon=True)
            ST = threading.Thread(target=self.server_listener, daemon=True)
            CT.start() ; ST.start()

            while CT.is_alive() or ST.is_alive():
                try:
                    time.sleep(0.178)
                except KeyboardInterrupt:                                        
                    return            
