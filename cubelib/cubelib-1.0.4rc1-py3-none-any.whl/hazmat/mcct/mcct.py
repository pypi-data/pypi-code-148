from .tcp import TCPConnection
import logging
from cubelib import proto, state, NextState, bound
import cubelib
import time

class MinecraftConnection(TCPConnection):

    state: state = state.Handshaking
    compression: int = -1
    InboundBuffer: bytes = b""
    protocol: None
    
    def __init__(self, host, port, protocol, verbose=False):
        
        self._logger = logging.getLogger("MCConn")
        self._logger.setLevel(logging.DEBUG if verbose else logging.ERROR)
        self.protocol = protocol
        super().__init__(host, port)
   
    def packet_recieved(self, pack):
        pass

    def error_occured(self, err):
        self._logger.error(err)

    def sendp(self, pack):

        self._logger.debug(F"-> {pack}")
        self.send(pack.build(self.compression))
        t = pack.__class__
        if t is proto.ServerBound.Handshaking.Handshake:
            self.state = state.Status if pack.NextState == NextState.Status else state.Login
    
    def make_changes(self, pack):
        
        self._logger.debug(F"<- {str(pack)[:1000]}")
        t = pack.__class__
        if self.state is state.Login:
            if t is self.protocol.ClientBound.Login.SetCompression:
                self.compression = pack.Threshold

            if t is self.protocol.ClientBound.Login.LoginSuccess:
                self.state = state.Play

        if self.state is state.Play:
            if t is self.protocol.ClientBound.Play.KeepAlive:
                self.sendp(self.protocol.ServerBound.Play.KeepAlive(pack.KeepAliveID))

    def data_recieved(self, data):

        self.InboundBuffer += data
        pcks = []
        self.InboundBuffer = cubelib.readPacketsStream(self.InboundBuffer, self.compression, bound.Client, pcks)
        for p in pcks:            
            pack = p.resolve(self.state, self.protocol if self.state in (state.Login, state.Play) else proto)            
            self.make_changes(pack)
            self.packet_recieved(pack)

class StatusRetriver(MinecraftConnection):

    retrieved = False
    status = None
    ping = None
    ping_sent_time = 0
    
    with_ping = False
    proto_ver = 47

    def __init__(self, host, port, protocol=47, verbose=False):

        self.proto_ver = protocol
        self.host = host
        self.port = port
        self.verbose = verbose
    
    def connection_made(self):
        
        self.sendp(proto.ServerBound.Handshaking.Handshake(self.proto_ver, self.host, self.port, NextState.Status))
        self.state = state.Status
        self.sendp(proto.ServerBound.Status.Request())

    def packet_recieved(self, pack):

        t = pack.__class__
        if t is proto.ClientBound.Status.Response:
            self.status = pack.JsonRsp
            if not self.with_ping:
                self.retrieved = True
                self.alive = False
                return
            self.sendp(proto.ServerBound.Status.Ping(1337))
            self.ping_sent_time = time.time()

        if t is proto.ClientBound.Status.Pong:
            self.ping = round((time.time() - self.ping_sent_time)*1000)
            self.retrieved = True
            self.alive = False     
    
    def retrieve(self, ping=True):
        
        self.with_ping = ping        
        super().__init__(self.host, self.port, None, self.verbose)

        start_time = time.time()
        while (time.time() - start_time) < 1:           
            time.sleep(0.0) # context switch
            if self.retrieved:
                return self.status, self.ping
        self.alive = False
        raise TimeoutError("Failed to retrieve server status in time, timeout!")

class MinecraftClient(MinecraftConnection):

    def __init__(self, host, port, protocol, username, verbose=False):
                
        self.logger = logging.getLogger("MinecraftClient")
        self.logger.setLevel(logging.DEBUG if verbose else logging.ERROR)
        self.logger.info("Retrieving server status...")
        status, ping = StatusRetriver(host, port).retrieve()
        self.logger.info(status)
        self.logger.info(F"Ping: {ping}ms")

        self.protocol = protocol
        self.username = username
        super().__init__(host, port, protocol, False)

    def on_logon(uuid: str, username: str):
        pass

    def packet_recieved(self, pack):

        t = pack.__class__
        c = self.protocol.ClientBound
        if t is c.Login.LoginSuccess:
            self.on_logon(pack.UUID, pack.Username)

        if t is c.Login.Disconnect:
            self.on_disconnect(pack.Reason)
    
    def connection_made(self):

        self.sendp(proto.ServerBound.Handshaking.Handshake(self.protocol.version, self.host, self.port, NextState.Login))        
        self.sendp(self.protocol.ServerBound.Login.LoginStart(self.username))
                
