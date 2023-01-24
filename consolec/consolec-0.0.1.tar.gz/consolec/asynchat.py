import asyncio
import socket

HOST_IP = socket.gethostbyname(socket.gethostname())

class Server():

    def __init__(self, ip, port):
        
        self.__s__ = socket.socket()
        
        self.__ip__ = ip
        self.__port__ = port

    
    def bind(self, clients):

        self.__s__.bind((self.ip, self.port))
        self.__s__.listen(clients)


    def allow(self):

        self.__conn__, self.__addr__ = self.__s__.accept()

    
    async def getAsync(self, byte, encoding="utf8"):

        self.__msg__ = (self.__conn__.recv(byte)).decode(encoding)
        return self.__msg__
    
    async def sendAsync(self, message, encoding="utf8"):

        self.__conn__.send(message.encode("utf8"))

    
    def get(self, byte, encoding="utf8"):

        self.__msg__ = (self.__conn__.recv(byte)).decode(encoding)
        return self.__msg__
    
    def send(self, message, encoding="utf8"):

        self.__conn__.send(message.encode("utf8"))




class Client():

    def __init__(self, ip, port) -> None:
        
        self.__ip__ = ip
        self.__port__ = port

        self.__s__ = socket.socket()

    
    def connect(self):

        self.__s__.connect((self.__ip__, self.__port__))

    
    async def getAsync(self, byte, encoding="utf8"):

        self.__msg__ = (self.__s__.recv(byte)).decode(encoding)
        return self.__msg__
    
    async def sendAsync(self, message, encoding="utf8"):

        self.__s__.send(message.encode("utf8"))

    
    def get(self, byte, encoding="utf8"):

        self.__msg__ = (self.__s__.recv(byte)).decode(encoding)
        return self.__msg__
    
    def send(self, message, encoding="utf8"):

        self.__s__.send(message.encode("utf8"))

    