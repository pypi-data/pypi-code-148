
from asyncio import Queue, sleep
import asyncio
from enum import Enum
from multiprocessing.connection import Connection
from typing import Any, List, Tuple, Optional, AsyncGenerator
import os
import shutil
from xbridge.cipher import Cipher
from xbridge.inner_actions import get_handler_func
from xbridge.permission import Permission
from xbridge.rsa_key import RSAKey

from xbridge.session import Session, SessionRole, SessionState
from xbridge.transmsg import CompleteMsg, ConnectMsg, HelloMsg, NormalMsg, MsgType
from xbridge import file
from xbridge.config import Config
from xbridge.transdata import DataType, TransData

class FileInfo:

    path: str
    format: file.FileFormat

    uncompressed_dir: str # uncompressed dir

    cipher: Cipher
    process: Optional[Any] = None
    pipe: Optional[Connection] = None

    def __init__(self, cipher, process, pipe):
        self.process = process
        self.pipe = pipe
        self.cipher = cipher

    def setup_path(self, dir: str, name: str, format: file.FileFormat):

        fpath = os.path.join(dir, name)
        index = 1
        while os.path.exists(fpath):
            fpath = os.path.join(dir, '__temp_' + str(index), name)
            index += 1

        fpath_dir = os.path.dirname(fpath)
        if not os.path.isdir(fpath_dir):
            os.makedirs(fpath_dir, 0o755)
            
        self.path = fpath
        self.format = format

        if format == file.FileFormat.TarArchived:
            dirname = name.split(".tar")[0]
            print("dir name=", dirname)
            dirpath = os.path.join(dir, dirname)
            index = 1
            while os.path.exists(dirpath):
                dirpath = os.path.join(dir, '__temp_' + str(index), dirname)
                index += 1
            self.uncompressed_dir = dirpath
        else:
            self.uncompressed_dir = ''

        # print("fpath:", fpath)
        # print("uncompress:", self.uncompressed_dir)
    
class ChannelRole(Enum):
    Client = "client"
    Server = "server"

class Channel():

    # 正在接收文件信息
    receiving_file: Optional[FileInfo] = None

    # session info
    session: Session = None
    peerid: str

    # indicate channel finished or not
    finished = False

    # cipher for Normal Msg
    cipher: Optional[Cipher]

    # Permissions for client
    permission: Optional[Permission]

    event_queue: Queue

    role: ChannelRole

    ready: bool = False

    rsa_key: RSAKey

    def __init__(self, role: ChannelRole) -> None:
        self.permission = Permission.load(Config.config_dir)
        self.rsa_key = RSAKey.load(Config.config_dir)
        self.event_queue = asyncio.Queue()
        self.role = role
        print('[+] Channel init')

    def __del__(self):
        print('[-] Channel deleted')



    async def subscribe(self, subscriber):
        try:
            print("subscriber start...")
            async for message in subscriber:

                data = TransData.fromBytes(message)
                # print('got transdata[%d], type=%s' % (len(data.msg), data.type.name))

                if data.type in [ DataType.hello, DataType.connect, DataType.complete ]:
                    # self.on_pending_msg(data.type, data.resolveMsg())
                    await self.event_queue.put((data.type, data.resolveMsg()))
                    if data.type == DataType.complete:
                        break
                    continue

                # file receiving
                if data.type == DataType.file:
                    # print('file data msg[%d]' % len(data.msg), data.msg)
                    self.receiving_file.pipe.send(data.msg)
                    # await sleep(1)
                    continue

                # handle msg
                msg: NormalMsg = data.resolveMsg(self.cipher)
                # print('got Msg: %s' % msg.toPrettyString())

                if msg.type in [ MsgType.GetFile, MsgType.Reply, MsgType.Request, MsgType.Done, MsgType.Later, MsgType.Resume]:
                    # self.on_pending_msg(data.type, msg)
                    await self.event_queue.put((data.type, msg))
                    continue

                #
                # handle receive file
                #
                elif msg.type == MsgType.SendFileCipher:
                    key = bytes.fromhex(msg.params[0])
                    iv = bytes.fromhex(msg.params[1])
                    # start a new writer process
                    (c, process) = file.start_file_writer_process(key, iv)
                    self.receiving_file = FileInfo(Cipher(key, iv), process, c)

                elif msg.type == MsgType.SendFileInfo:
                    (name, size, format) = msg.params
                    self.receiving_file.setup_path(self.session.dir, name, format)
                    # print("got File info: %s (size=%d)" % (fpath, msg.params[1]))
                    self.receiving_file.pipe.send((self.receiving_file.path, int(size)))
                    
                elif msg.type == MsgType.SendFileEnd:
                    self.finish_file_write_process()
                    if self.receiving_file.format == file.FileFormat.TarArchived:
                        # untar
                        shutil.unpack_archive(self.receiving_file.path, self.receiving_file.uncompressed_dir, "tar")
                    await self.event_queue.put((data.type, msg))
        
        except Exception as e:
            print("subscriber error:", e)
            raise e
        finally:
            print("subscriber will end!")
            self.finish_file_write_process()
            self.finished = True
            # self.on_pending_msg(DataType.complete, None)
            await self.event_queue.put((DataType.complete, CompleteMsg(reason="subscriber end")))
            print("subscriber end!")

    def finish_file_write_process(self):
        if self.receiving_file:
            if self.receiving_file.process:
                self.receiving_file.pipe.send(('', 0))
                self.receiving_file.process.join()
                self.receiving_file.process = None


    async def wait_for_msg(self, datatypes: List[DataType] = [], msgtypes: List[MsgType] = []) -> any:
        print('wait_for: ', datatypes, msgtypes, "...")

        datatype, _msg = await self.event_queue.get()
        print("wait got ", datatype)

        if datatype in datatypes:
            # print('match DataType: %s!' % (datatype.name))
            return _msg 

        if datatype == DataType.complete:
            # should close
            complete: CompleteMsg = _msg
            raise Exception("connection will close. reason: %s" % complete.reason)

        if len(msgtypes) > 0:

            if datatype != DataType.encrypted:
                raise Exception("received data must be encrypted! msg=", _msg)

            msg: NormalMsg = _msg
            #print('wait got %s' % msg.toString())

            if msg.type in msgtypes:
                # print('match MsgType: %s!' % (msg.type.name))
                return msg

            if msg.type == MsgType.Done:
                raise Exception("session will done!")


        raise Exception("received unknown msg %s" % _msg)
    

    async def wait_on_sending_for(self, msgtypes: List[MsgType] = []) -> AsyncGenerator[Tuple[bytes, any], None]:

        msg: NormalMsg

        msgtypes_with_getfile = [MsgType.GetFile, MsgType.Later, MsgType.Done] + msgtypes

        print("wait_on_sending_for", msgtypes)
        while True:

            msg = await self.wait_for_msg(msgtypes=msgtypes_with_getfile)
            if msg.type in msgtypes:
                break

            if msg.type == MsgType.Later:
                raise Exception("session will resume later")

            if msg.type == MsgType.Done:
                raise Exception("session will done")

            if msg.type != MsgType.GetFile:
                raise Exception("wait got unexpected msg", msg)

            # handle request files: send a file/dir
            p = msg.params[0]
            if p not in self.session.files_provided or not os.path.exists(p):
                print("warn: Failed to get a file not provided!!", p)
                yield TransData.encrypted(NormalMsg(MsgType.SendFileEnd), self.cipher).toBytes()
                continue
            norm_path = os.path.abspath(p)
            async for e in file.file_generator(norm_path, self.session.dir, self.cipher):
                yield e, None

        yield None, msg


    async def request_file(self, filename: str, received_files: List[str] = []) -> AsyncGenerator[bytes, None]:

        print('Try request file ', filename)

        self.receiving_file = None

        # send request for a file/dir
        yield TransData.encrypted(NormalMsg(MsgType.GetFile, sessionid=self.session.id, params=[filename]), self.cipher).toBytes()

        # wait for file received
        print('waiting for file received ...')
        await self.wait_for_msg(msgtypes=[MsgType.SendFileEnd])

        # await self.got_file_event.wait()
        print('GOT a file/dir!')
        if self.receiving_file.uncompressed_dir:
            received_files.append(self.receiving_file.uncompressed_dir)
        else:
            received_files.append(self.receiving_file.path)


    async def handshake(self) -> AsyncGenerator[bytes, None]:
        datatype: DataType
        _msg: any
        random: bytes
        print("myid:", self.rsa_key.pubkey_hash)
        
        if self.role == ChannelRole.Client:
            # send hello
            random = Cipher.random()
            yield TransData.hello(self.rsa_key.pubkey_hex, random).toBytes()

        # wait hello
        hello_msg: HelloMsg = await self.wait_for_msg(datatypes=[DataType.hello])
        # if datatype == DataType.complete:
        #     raise Exception("oh, unexpected finish!")

        # got hello from peer
        pubkey = bytes.fromhex(hello_msg.pubkey)
        peerRSA = RSAKey.fromBytes(None, pubkey)
        peerRandom = hello_msg.random

        self.peerid = peerRSA.pubkey_hash
        print("peerid:", self.peerid)

        if self.role == ChannelRole.Server:
            # check connection permission
            pkh = peerRSA.pubkey_hash
            if not self.permission.allowConnect(pkh):
                # reply refuse
                print("❌ Refused to connect with ", pkh)
                yield TransData.complete('refuse to connect with %s' % pkh).toBytes()
                return

            # send hello ack
            random = Cipher.random()
            yield TransData.hello(self.rsa_key.pubkey_hex, random).toBytes()


        if self.role == ChannelRole.Client:
            # new cipher
            self.cipher = Cipher.new()

            # send connect
            ekey = peerRSA.encrypt(self.cipher.key)
            eiv = peerRSA.encrypt(self.cipher.iv)
            sign = self.rsa_key.sign(ekey + eiv + random + peerRandom)
            # yield TransData.hello(self.rsa_key.pubkey_hex, random).toBytes()
            yield TransData.connect(ekey.hex(), eiv.hex(), sign.hex()).toBytes()
        
        # waiting for connect
        connect_msg = await self.wait_for_msg(datatypes=[DataType.connect])

        if self.role == ChannelRole.Server:

            # check signature
            ekey = bytes.fromhex(connect_msg.key)
            eiv = bytes.fromhex(connect_msg.iv)
            if not peerRSA.verify(ekey + eiv + peerRandom + random, bytes.fromhex(connect_msg.sign)):
                print("verify failed!!!")
                yield TransData.complete('connection verify failed %s' % pkh).toBytes()
                return

            # init cipher
            key = self.rsa_key.decrypt(ekey)
            iv = self.rsa_key.decrypt(eiv)
            self.cipher = Cipher(key, iv)

            # agree, send connect ack
            yield TransData.connect(empty=True).toBytes()
        
        self.ready = True


    async def run_publisher(self, init_msg: Optional[NormalMsg], handle_reply=None) -> AsyncGenerator[bytes, None]:

        async for e in self.handshake():
            yield e

        if not self.ready :
            print("Handshake failed!")
            return

        print("🤝 Handshake Success!")


        if self.role == ChannelRole.Server:
            # server
            # waiting for request
            init_msg: NormalMsg = await self.wait_for_msg(msgtypes=[MsgType.Request, MsgType.Resume ])
            print('got request/resume:', init_msg.toPrettyString())

        if init_msg.type == MsgType.Request:
            if self.role == ChannelRole.Client:
                role = SessionRole.Initiator
            else:
                role = SessionRole.Handler
            self.session = Session(init_msg.sessionid, self.peerid, role)
        else:
            # init_msg is resume
            self.session = Session(init_msg.sessionid, self.peerid)
            if self.role == ChannelRole.Client:
                yield TransData.encrypted(NormalMsg(MsgType.Resume, init_msg.sessionid), self.cipher).toBytes()

        # session prepared
        self.session.dump()


        if self.session.state == SessionState.Initial:
            if init_msg.type != MsgType.Request:
                raise Exception("msg should be request")

            self.session.request = init_msg
            if self.session.role == SessionRole.Initiator:
                # Initiator
                print('will send request:', init_msg.toPrettyString())
                # 1. send request now
                yield TransData.encrypted(init_msg, self.cipher).toBytes()
                if init_msg.files:
                    self.session.files_provided = init_msg.files
            else:
                # Handler
                # check permission for this request
                if not self.permission.allowAction(self.peerid, init_msg.action):
                    # yield TransData.refuse('refuse to connect with %s' % pkh ).toBytes()
                    print("Refused action ", init_msg.action)
                    yield TransData.encrypted(NormalMsg.reply(init_msg.app, init_msg.action, ['refused action']), self.cipher).toBytes()
                    return
                if init_msg.files:
                    self.session.files_accessable = init_msg.files  
            self.session.state = SessionState.RequestTransferring


        if self.session.state == SessionState.RequestTransferring:
            if self.session.role == SessionRole.Initiator:
                # 2. waiting for reply/later/get_file
                async for e, _msg in self.wait_on_sending_for([MsgType.Reply]):
                    if e:
                        yield e
                # if datatype == DataType.complete:
                #     print("complete abnormal!!!")
                #     return

                reply: NormalMsg = _msg

                # got later
                if reply.type == MsgType.Later:
                    print("🀄️ session paused. ", self.session.id)
                    return

                # got reply
                self.session.state = SessionState.ReplyTransferring
                self.session.reply = reply
                if reply.files:
                    self.session.files_accessable = reply.files
            else:
                # handler
                # receive all files in request
                received_files = []
                for filename in self.session.files_accessable:
                    async for e in self.request_file(filename, received_files):
                        yield e

                self.session.state = SessionState.RequestReceived

                # print("action type:", type(self.session.request.action))
                handle = get_handler_func(self.session.request.action)
                if handle is None:
                    print("🀄️ Don't support action \"%s\"" % self.session.request.action)
                    yield TransData.encrypted(NormalMsg(MsgType.Later), self.cipher).toBytes()
                    return

                # handle request
                async for m in handle(init_msg, received_files):
                    self.session.reply = m
                    

        if self.session.state == SessionState.RequestReceived:
            if self.session.role != SessionRole.Handler:
                raise Exception("RequestReceived only for Handler")
            if init_msg.type == MsgType.Reply:
                self.session.reply = init_msg
            reply = self.session.reply
            if reply is None:
                raise Exception("Reply msg is none!")
            print('will send reply:', reply.toPrettyString())
            self.session.files_provided = reply.files
            yield TransData.encrypted(reply, self.cipher).toBytes()
            self.session.state = SessionState.ReplyTransferring


        if self.session.state == SessionState.ReplyTransferring:
            if self.session.role == SessionRole.Initiator:
                # 3. get files in reply
                received_files = []
                # receive all files into this session
                for filename in self.session.files_accessable:
                    async for e in self.request_file(filename, received_files):
                        yield e

                print("got reply:", reply.toPrettyString())

                # custom handle reply
                if handle_reply:
                    # print('call custom handle reply')
                    handle_reply(reply, received_files)

                # 4. done
                yield TransData.encrypted(NormalMsg(MsgType.Done), self.cipher).toBytes()

            else:
                # Handler
                # wait for done
                async for data, msg in self.wait_on_sending_for([MsgType.Done]):
                    if data:
                        yield data

        print("👌Session Done!")
        self.session.state = SessionState.Done


    async def publisher(self, init_msg: NormalMsg = None, handle_reply=None) -> AsyncGenerator[bytes, None]:
        try:
            print('publisher start...')
            async for e in self.run_publisher(init_msg, handle_reply):
                yield e
        except Exception as e:
            print("❌", e)
            if not self.finished:
                # publisher end first, tell peer connection will close
                yield TransData.complete("%s" % e).toBytes()
                self.finished = True
            raise e
        finally:
            print("publisher end")
            if not self.finished:
                # publisher end first, tell peer connection will close
                yield TransData.complete('publisher end').toBytes()
            
            self.finished = True
            self.session.save()
            # self.finished_event.set()
            
