import socket
import threading

class TCPConnection(object):

    socket: socket.socket
    thread: threading.Thread
    alive: bool = True

    def __init__(self, host, port):
        
        self.host = host
        self.port = port
        self.socket = socket.socket(2, 1)
        self.socket.settimeout(1)
        try:
            self.socket.connect((host, port))
        except Exception as e:            
            self.error_occured(e)
            self.alive = False
            return
        self.socket.settimeout(None)
        self.socket.setblocking(0)
        self.connection_made()

        self.thread = threading.Thread(target=self._poll_loop)
        self.thread.start()        
    
    def _poll_loop(self):

        while self.alive:            
            try:
                data = self.socket.recv(65535)
            except Exception as e:
                if isinstance(e, BlockingIOError):
                    continue
                self.connection_lost(e)
                self.socket.close()
                self.alive = False
                break

            if not data:
                self.connection_lost(None)
                self.socket.close()
                self.alive = False
                break

            self.data_recieved(data)
        
    def shutdown(self):
        self.alive = False        
        #self.socket.close()       

    def send(self, data):
        try:
            self.socket.sendall(data)
        except Exception as e:
            self.error_occured(e)
            self.alive = False

    def connection_made(self):
        pass
    
    def connection_lost(self, error):
        pass
    
    def data_recieved(self, data):
        pass

    def error_occured(self, error):
        pass